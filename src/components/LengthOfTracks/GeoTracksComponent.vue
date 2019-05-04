<template>
  <svg :width="width" :height="height" ref="svg">
    <rect x="0" y="0" rx="20" ry="20" :width="width" :height="height" class="bg" />
    <g class="g-map">
      <g>
        <path :d="regionsPath" class="regions" />
      </g>
      <g ref="map" />
    </g>
    <g class="g-chart" ref="chart">
      <text :x="margin.left" :y="margin.top - 10">Top {{ nr }}</text>
    </g>
  </svg>
</template>

<script>
import d3 from '@/assets/d3';

export default {
  props: {
    geojson: {
      type: Object,
      required: true,
    },
    regions: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      width: 1000,
      height: 600,
      chartWidth: 300,
      chartHeight: 550,
      margin: {
        top: 30, right: 20, bottom: 20, left: 100,
      },
      center: d3.geoCentroid(this.geojson),
      nr: 40,
      pathFnNr: 0,
      mapScale: 10000,
      delay: 60,
      duration: 4000,
    };
  },
  mounted() {
    this.init();
  },
  computed: {
    projection() {
      return d3.geoMercator()
        .center(this.center)
        .scale(this.mapScale)
        .translate([this.width / 2 + this.margin.left + 30, this.height / 2 - 50]);
    },
    pathGeo() {
      return d3.geoPath().projection(this.projection);
    },
    topFeatures() {
      return [...this.geojson.features]
        .sort((a, b) => b.properties.length - a.properties.length)
        .filter((item, index) => index < this.nr);
    },
    scale() {
      const x = d3.scaleLinear()
        .range([0, this.chartWidth])
        .domain([0, Math.max(...this.topFeatures.map(f => f.properties.length))]);
      const y = d3.scaleBand()
        .range([0, this.chartHeight])
        .domain(this.topFeatures.map(f => f.properties.trackcode))
        .padding(0.1);
      const color = d3.scaleSequential(d3.interpolateYlOrBr)
        .domain([0, Math.max(...this.topFeatures.map(f => f.properties.length))]);
      return { x, y, color };
    },
    pathFn() {
      return this.pathFnNr === 0 ? this.pathRectangle : this.pathGeo;
    },
    regionsPath() {
      return this.pathGeo(this.regions);
    },
  },
  methods: {
    init() {
      d3.select(this.$refs.map)
        .selectAll('path.track').data(this.geojson.features)
        .enter()
        .append('path')
        .attr('class', 'track')
        .attr('d', this.pathGeo)
        .on('mouseover', this.highlight)
        .on('mouseout', this.unhighlight);

      d3.select(this.$refs.chart)
        .selectAll('path.chart-bg').data(this.topFeatures)
        .enter()
        .append('path')
        .attr('class', 'chart-bg')
        .attr('d', this.pathRectangleBg)
        .on('mouseover', this.highlight)
        .on('mouseout', this.unhighlight);

      d3.select(this.$refs.chart)
        .selectAll('path.chart').data(this.topFeatures)
        .enter()
        .append('path')
        .attr('class', 'chart')
        .style('stroke', d => this.scale.color(d.properties.length))
        .attr('d', this.pathRectangle)
        .on('mouseover', this.highlight)
        .on('mouseout', this.unhighlight);

      d3.select(this.$refs.chart)
        .selectAll('text.chart-text').data(this.topFeatures)
        .enter()
        .append('text')
        .attr('class', 'chart-text')
        .attr('x', this.margin.left - 4)
        .attr('y', d => this.margin.top
          + this.scale.y(d.properties.trackcode) + (this.scale.y.bandwidth() / 2) + 3)
        .text(d => `${d.properties.trackcode} (${Math.round(d.properties.length / 1000)} km)`)
        .on('mouseover', this.highlight)
        .on('mouseout', this.unhighlight);
    },
    pathRectangleBg(feature) {
      const x0 = this.margin.left;
      const x1 = this.margin.left + this.scale.x(feature.properties.length);
      const y0 = this.margin.top
        + this.scale.y(feature.properties.trackcode) + (this.scale.y.bandwidth() / 2);

      return `M${x0} ${y0}L${x1} ${y0}`;
    },
    pathRectangle(feature) {
      // eslint-disable-next-line
      const mergedCoordinates = [].concat.apply([], feature.geometry.coordinates);
      const x1 = this.scale.x(feature.properties.length);
      const y0 = this.margin.top
        + this.scale.y(feature.properties.trackcode) + (this.scale.y.bandwidth() / 2);

      // we need to have the same number of points than on the map
      // so we divide the line in equal parts
      let points = '';
      let i = 0;
      let p1 = `${this.margin.left} ${y0}`;
      feature.geometry.coordinates.forEach((subpath) => {
        points += `M${p1}`;
        subpath.forEach((v, j) => {
          p1 = `${this.margin.left + ((x1 * (i + 1)) / mergedCoordinates.length)} ${y0}`;
          if (j !== 0) {
            points += `L${p1}`;
          }
          i += 1;
        });
      });

      return points;
    },
    animate() {
      this.pathFnNr = (this.pathFnNr + 1) % 2;
      d3.select(this.$refs.chart)
        .selectAll('path.chart')
        .transition()
        .duration(this.duration)
        .delay((d, i, nodes) => {
          if (this.pathFnNr === 1) {
            return i * this.delay;
          }
          return (nodes.length - 1 - i) * this.delay;
        })
        .attr('d', this.pathFn);
    },
    highlight(feature) {
      d3.select(this.$refs.svg)
        .selectAll('path.chart, text.chart-text, path.track')
        .filter(d => d.properties.trackcode === feature.properties.trackcode)
        .classed('highlighted', true);
    },
    unhighlight() {
      d3.select(this.$refs.svg)
        .selectAll('path.chart, text.chart-text, path.track')
        .classed('highlighted', false);
    },
  },
};
</script>

<style scoped>
  .bg {
    fill: rgb(240, 240, 240);
  }
  svg >>> .track {
    stroke-width: 1px;
    stroke: steelblue;
    stroke-linecap: round;
    fill: none;
  }
  svg >>> .chart {
    stroke-width: 4px;
    stroke: white;
    stroke-linecap: round;
    fill: none;
  }
  svg >>> .chart-bg {
    stroke-width: 2px;
    stroke: white;
    stroke-linecap: round;
    fill: none;
  }
  svg >>> .chart-text {
    text-anchor: end;
    font-size: 8pt;
  }
  svg >>> .regions {
    fill: white;
    stroke: darkgrey;
    stroke-width: 1px;
  }
  svg >>> .highlighted {
    stroke-width: 6px;
    font-weight: bold;
  }
</style>
