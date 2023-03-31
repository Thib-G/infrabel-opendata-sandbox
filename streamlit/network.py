# run with:
# streamit run network.py

import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config


@st.cache_data
def import_trains():
    # return pd.read_csv('https://fr.ftp.opendatasoft.com/infrabel/PunctualityHistory/Data_raw_punctuality_202302.csv')
    # download locally to improve perf:
    # `wget https://fr.ftp.opendatasoft.com/infrabel/PunctualityHistory/Data_raw_punctuality_202302.csv``
    return pd.read_csv('Data_raw_punctuality_202302.csv')


@st.cache_data
def import_ptcars():
    # df = pd.read_json('https://opendata.infrabel.be/api/explore/v2.1/catalog/datasets/operationele-punten-van-het-newterk/exports/json?lang=fr&timezone=Europe%2FBerlin')
    df = pd.read_json('operationele-punten-van-het-newterk.json')
    df['lat'] = df['geo_shape'].apply(lambda x: x['geometry']['coordinates'][1])
    df['lon'] = df['geo_shape'].apply(lambda x: x['geometry']['coordinates'][0])
    del df['geo_point_2d']
    del df['geo_shape']
    return df

@st.cache_data
def prepare_trains(df):
    
    # Repair DataFrame
    df.loc[pd.isnull(df['PLANNED_TIME_ARR']), 'PLANNED_TIME_ARR'] = df.loc[pd.isnull(df['PLANNED_TIME_ARR']),'PLANNED_TIME_DEP']
    df.loc[pd.isnull(df['PLANNED_TIME_DEP']), 'PLANNED_TIME_DEP'] = df.loc[pd.isnull(df['PLANNED_TIME_DEP']),'PLANNED_TIME_ARR']
    df.loc[pd.isnull(df['REAL_TIME_ARR']), 'REAL_TIME_ARR'] = df.loc[pd.isnull(df['REAL_TIME_ARR']),'REAL_TIME_DEP']
    df.loc[pd.isnull(df['REAL_TIME_DEP']), 'REAL_TIME_DEP'] = df.loc[pd.isnull(df['REAL_TIME_DEP']),'REAL_TIME_ARR']
    df.loc[pd.isnull(df['PLANNED_DATE_ARR']), 'PLANNED_DATE_ARR'] = df.loc[pd.isnull(df['PLANNED_DATE_ARR']),'PLANNED_DATE_DEP']
    df.loc[pd.isnull(df['PLANNED_DATE_DEP']), 'PLANNED_DATE_DEP'] = df.loc[pd.isnull(df['PLANNED_DATE_DEP']),'PLANNED_DATE_ARR']
    df.loc[pd.isnull(df['REAL_DATE_ARR']), 'REAL_DATE_ARR'] = df.loc[pd.isnull(df['REAL_DATE_ARR']),'REAL_DATE_DEP']
    df.loc[pd.isnull(df['REAL_DATE_DEP']), 'REAL_DATE_DEP'] = df.loc[pd.isnull(df['REAL_DATE_DEP']),'REAL_DATE_ARR']
    df.loc[pd.isnull(df['LINE_NO_DEP']), 'LINE_NO_DEP'] = 'noline'
    df['i'] = df.index

    # Create edges in SQL with DuckDB
    sql = """
        WITH sq AS (
            SELECT
                strptime(DATDEP, '%d%b%Y') AS DATDEP,
                TRAIN_NO,
                RELATION,
                TRAIN_SERV,
                PTCAR_NO,
                LINE_NO_DEP,
                CAST(strptime(REAL_DATE_ARR,    '%d%b%Y') AS DATE) + CAST(strptime(REAL_TIME_ARR,    '%-H:%M:%S') AS TIME) AS REAL_DT_ARR,
                CAST(strptime(REAL_DATE_DEP,    '%d%b%Y') AS DATE) + CAST(strptime(REAL_TIME_DEP,    '%-H:%M:%S') AS TIME) AS REAL_DT_DEP,
                CAST(strptime(PLANNED_DATE_ARR, '%d%b%Y') AS DATE) + CAST(strptime(PLANNED_TIME_ARR, '%-H:%M:%S') AS TIME) AS PLANNED_DT_ARR,
                CAST(strptime(PLANNED_DATE_DEP, '%d%b%Y') AS DATE) + CAST(strptime(PLANNED_TIME_DEP, '%-H:%M:%S') AS TIME) AS PLANNED_DT_DEP,
                DELAY_ARR,
                DELAY_DEP,
                PTCAR_LG_NM_NL,
                LINE_NO_ARR,
                i,
            FROM
                df
        ), shifted AS (
            SELECT
                *,
                LEAD(PTCAR_LG_NM_NL) OVER w AS NEXT_PTCAR_LG_NM_NL,
                LEAD(LINE_NO_ARR) OVER w AS NEXT_LINE_NO_ARR,
                LEAD(PTCAR_NO) OVER w AS NEXT_PTCAR_NO,
                LEAD(LINE_NO_DEP) OVER w AS NEXT_LINE_NO_DEP,
                LEAD(REAL_DT_ARR) OVER w AS NEXT_REAL_DT_ARR,
                LEAD(REAL_DT_DEP) OVER w AS NEXT_REAL_DT_DEP,
                LEAD(PLANNED_DT_ARR) OVER w AS NEXT_PLANNED_DT_ARR,
                LEAD(PLANNED_DT_DEP) OVER w AS NEXT_PLANNED_DT_DEP,
            FROM
                sq
            WINDOW w AS (PARTITION BY TRAIN_NO, DATDEP ORDER BY i)
        )
        SELECT
            DATDEP,
            TRAIN_NO,
            RELATION,
            DELAY_DEP,
            DELAY_ARR,
            REAL_DT_ARR,
            REAL_DT_DEP,
            PLANNED_DT_ARR,
            PLANNED_DT_DEP,
            EXTRACT('epoch' FROM (NEXT_REAL_DT_DEP - REAL_DT_DEP)) AS REAL_TIME,
            EXTRACT('epoch' FROM (NEXT_PLANNED_DT_DEP - PLANNED_DT_DEP)) AS PLANNED_TIME,
            EXTRACT('epoch' FROM (REAL_DT_DEP - PLANNED_DT_DEP)) AS DELAY_DEP_CALC,
            PTCAR_LG_NM_NL || '_' || LINE_NO_DEP AS NODE_1,
            PTCAR_LG_NM_NL AS PTCAR_1,
            LINE_NO_DEP AS LINE_NO_1,
            PTCAR_NO AS PTCAR_ID_1,
            NEXT_PTCAR_LG_NM_NL || '_' || NEXT_LINE_NO_DEP AS NODE_2,
            NEXT_PTCAR_LG_NM_NL AS PTCAR_2,
            NEXT_LINE_NO_DEP AS LINE_NO_2,
            NEXT_PTCAR_NO AS PTCAR_ID_2,
            EXTRACT('hour' FROM REAL_DT_DEP) AS HOUR,
        FROM
            shifted
        WHERE
            NEXT_PTCAR_NO IS NOT NULL
        ORDER BY
            DATDEP, TRAIN_NO, REAL_DT_DEP
    """
    return duckdb.sql(sql).df()


@st.cache_data
def get_ptcars(df):
    sql = """
        SELECT DISTINCT
            PTCAR_1
        FROM
            df
        ORDER BY
            1
    """
    return duckdb.sql(sql).df()


def get_stats_by_station(df, ptcar='CHARLEROI-CENTRAL'):
    return df.loc[
            df['PTCAR_1'] == ptcar,:
        ].groupby([
            'LINE_NO_1',
            'LINE_NO_2',
            'PTCAR_2'
        ])['REAL_TIME'].aggregate(['count', 'min', 'median', 'mean', 'max'])


def get_delays_by_dow(df, ptcar='CHARLEROI-CENTRAL'):
    sql = """
        SELECT
            DATDEP,
            TRAIN_NO,
            PTCAR_1,
            PTCAR_2,
            REAL_DT_DEP,
            EXTRACT('epoch' FROM CAST(REAL_DT_DEP AS TIME)) / 3600.0 AS TIME_DEP,
            DELAY_DEP,
            EXTRACT('HOUR' FROM REAL_DT_DEP) AS HOUR,
            EXTRACT('DOW' FROM REAL_DT_DEP) AS DOW,
            CASE WHEN EXTRACT('DOW' FROM REAL_DT_DEP) IN (0, 6) THEN 'weekend'
                 ELSE 'week'
            END AS DAYTYPE,
        FROM
            df
        WHERE
            PTCAR_1 = ?
        ORDER BY
            6
    """
    with duckdb.connect() as con:
        result = con.execute(sql, [ptcar]).df()
    return result


def get_linked_ptcars(df_trains, df_ptcars_attributes, ptcar='CHARLEROI-CENTRAL'):
    sql = """
        SELECT DISTINCT
            ptcarid,
            longnamedutch,
            longnamefrench,
            taftapcode,
            symbolicname,
            lat,
            lon
        FROM
            df_trains
        JOIN
            df_ptcars_attributes
            ON df_ptcars_attributes.longnamedutch = df_trains.PTCAR_2
        WHERE
            df_trains.PTCAR_1 = ?
        ORDER BY
            1
    """
    with duckdb.connect() as con:
        result = con.execute(sql, [ptcar]).df()
    return result


st.write("""
    # Station stats

    Stats by station from [Infrabel Open Data](https://opendata.infrabel.be/explore/dataset/stiptheid-gegevens-maandelijksebestanden/information/)
""")


df_raw = import_trains()
df_trains = prepare_trains(df_raw)
df_ptcars = get_ptcars(df_trains)
df_ptcars_attributes = import_ptcars()


st.write("""
    ## PTCARs

    Select PTCAR
""")
ptcar = st.selectbox(
    label='PTCAR',
    options=df_ptcars,
    index=int(df_ptcars.index[df_ptcars['PTCAR_1'] == 'CHARLEROI-CENTRAL'][0]),
)

st.write(f"""
    ## Stats for {ptcar}
""")
         
st.write(get_stats_by_station(df_trains, ptcar))


st.write(f"""
    ## Delays in {ptcar}
""")

fig = px.scatter(get_delays_by_dow(df_trains, ptcar), x="TIME_DEP", y="DELAY_DEP", color="DAYTYPE", marginal_x="histogram")
st.plotly_chart(fig, theme=None, use_container_width=True)

st.write("""
    ## Linked PTCARs
""")

linked_ptcars = get_linked_ptcars(df_trains, df_ptcars_attributes, ptcar)

st.write(linked_ptcars)


def create_agraph(nodes, edges):
    n = [
        Node(
            id=i,
            label=node,
            title=node,
        )
        for i, node
        in nodes
    ]
    e = [
        Edge(
            source=node_from,
            label='connects',
            target=node_to
        )
        for node_from, node_to
        in edges
    ]
    config = Config(
        width=750,
        height=450,
        directed=True, 
        physics=True, 
        hierarchical=False,
        # **kwargs
    )

    return agraph(nodes=n, edges=e, config=config)


nodes = [(i, node) for i, node in enumerate([ptcar] + linked_ptcars['longnamefrench'].values.tolist())]
edges = [(0, i + 1) for i, _ in enumerate(nodes[1:])]

create_agraph(nodes, edges)


st.map(data=linked_ptcars)
