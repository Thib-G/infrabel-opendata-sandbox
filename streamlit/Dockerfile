# app/Dockerfile

FROM python:3.10-slim

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && wget -O Data_raw_punctuality_202302.csv https://fr.ftp.opendatasoft.com/infrabel/PunctualityHistory/Data_raw_punctuality_202302.csv \
    && wget -O operationele-punten-van-het-newterk.json https://opendata.infrabel.be/api/explore/v2.1/catalog/datasets/operationele-punten-van-het-newterk/exports/json?lang=fr&timezone=Europe%2FBerlin

RUN pip install -r requirements.txt

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "network.py", "--server.port=80", "--server.address=0.0.0.0"]
