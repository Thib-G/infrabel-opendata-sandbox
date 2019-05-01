<template>
  <svg :width="width" :height="height" ref="svg">
    <rect x="0" y="0" :width="width" :height="height" class="bg" />
    <g class="g-map">
      <g>
        <path :d="regionsPath" class="regions" />
      </g>
      <g ref="map" />
    </g>
    <g class="g-chart" ref="chart" />
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
      width: 800,
      height: 600,
      chartWidth: 300,
      chartHeight: 550,
      margin: {
        top: 30, right: 20, bottom: 20, left: 100,
      },
      center: d3.geoCentroid(this.geojson),
      nr: 40,
      pathFnNr: 0,
      mapScale: 8000,
      duration: 5000,
    };
  },
  mounted() {
    this.init();
  },
  computed: {
    projection() {
      return d3.geoMercator()
        .center(this.center)
        .scale(this.mapScale);
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
        .selectAll('path').data(this.geojson.features)
        .enter()
        .append('path')
        .attr('class', 'track')
        .attr('d', this.pathGeo);

      d3.select(this.$refs.chart)
        .selectAll('path').data(this.topFeatures)
        .enter()
        .append('path')
        .attr('class', 'chart')
        .style('stroke', d => this.scale.color(d.properties.length))
        .attr('d', this.pathRectangle);

      d3.select(this.$refs.chart)
        .selectAll('text').data(this.topFeatures)
        .enter()
        .append('text')
        .attr('class', 'chart-text')
        .attr('x', this.margin.left - 4)
        .attr('y', d => this.margin.top
          + this.scale.y(d.properties.trackcode) + (this.scale.y.bandwidth() / 2) + 3)
        .text(d => `${d.properties.trackcode} (${Math.round(d.properties.length / 1000)} km)`);
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
      let p1 = '';
      feature.geometry.coordinates.forEach((subpath) => {
        subpath.forEach((v, j) => {
          p1 = `${this.margin.left + ((x1 * i) / mergedCoordinates.length)} ${y0}`;
          if (j === 0) {
            points += 'M';
          } else {
            points += 'L';
          }
          points += `${p1}`;
          i += 1;
        });
      });

      return `${points}`;
    },
    animate() {
      this.pathFnNr = (this.pathFnNr + 1) % 2;
      const transition = d3.transition().duration(this.duration);
      d3.select(this.$refs.chart)
        .selectAll('path.chart')
        .transition(transition)
        .attr('d', this.pathFn);
    },
  },
};
</script>

<style scoped>
  .bg {
    fill: lightgrey;
  }
  svg >>> .track {
    stroke-width: 1px;
    stroke: steelblue;
    fill: none;
  }
  svg >>> .chart {
    stroke-width: 4px;
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
</style>
