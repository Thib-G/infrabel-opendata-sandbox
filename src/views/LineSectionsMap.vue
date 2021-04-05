<template>
  <div>
    <p>
      Show line sections with attributes. Select property:
      <select v-model="selected">
        <option v-for="p in propList" :key="p" :value="p">{{ p }}</option>
      </select>
      <br />Legend below.
    </p>
    <div class="map" ref="map">
    </div>
    <h3>Legend: {{ selected }}</h3>
    <p>
      <ul>
        <li v-for="v in scaleColor.domain()" :key="v">
          <svg width="20" height="10">
            <line class="legend-line" x1="0" x2="20" y1="5" y2="5"
              :style="{ stroke: scaleColor(v) }" />
          </svg> {{ v }}
        </li>
      </ul>
    </p>
    <h3>Sources</h3>
    <p><a href="https://opendata.infrabel.be/explore/dataset/lijnsecties"
      target="_blank">Section de lignes</a></p>
    <p>This map retrieves the data directly from Infrabel Open Data portal using the API:</p>
    <p><tt>https://opendata.infrabel.be/api/v2/catalog/datasets/lijnsecties/exports/geojson?rows=-1&amp;timezone=UTC&amp;pretty=false</tt></p>
  </div>
</template>

<script>
// @ is an alias to /src
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

import InfrabelService from '@/services/infrabel-service';
import d3 from '@/assets/d3';
import basemaps from '@/assets/map/basemaps';

// eslint-disable-next-line
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  // eslint-disable-next-line
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  // eslint-disable-next-line
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  // eslint-disable-next-line
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

export default {
  data() {
    return {
      map: undefined,
      infrabelService: InfrabelService,
      zoom: 8,
      belgiumCenterLatLng: [50 + (38 / 60) + (28 / 3600), 4 + (40 / 60) + (5 / 3600)],
      basemaps: basemaps(),
      selected: 'nrtracks',
      featureGroup: L.featureGroup(),
      lineSections: undefined,
    };
  },
  mounted() {
    this.initMap();
    this.getLineSections();
  },
  watch: {
    byValues() {
      this.updateLineSections();
    },
    selected() {
      this.updateLineSections();
    },
  },
  computed: {
    propList() {
      if (!this.lineSections) {
        return [];
      }
      return Object.keys(this.lineSections.features[0].properties);
    },
    byValues() {
      if (!this.lineSections) {
        return [];
      }
      return d3.nest()
        .key((d) => d.properties[this.selected])
        .entries(this.lineSections.features);
    },
    scaleColor() {
      return d3.scaleOrdinal()
        .range(d3.schemeCategory10)
        .domain(this.byValues.map((d) => d.key));
    },
  },
  methods: {
    initMap() {
      this.map = L.map(this.$refs.map, {
        center: this.belgiumCenterLatLng,
        zoom: this.zoom,
      });
      this.basemaps.light.addTo(this.map);
      L.control.layers(this.basemaps).addTo(this.map);
      this.featureGroup.addTo(this.map);
    },
    getLineSections() {
      this.infrabelService.getLineSections().then((data) => {
        this.lineSections = data;
      });
    },
    updateLineSections() {
      this.featureGroup.clearLayers();
      this.byValues.forEach((v) => {
        const geoJson = L.geoJson(v.values, {
          onEachFeature: (feature, layer) => {
            const popupHTML = document.createElement('div');
            let contentHTML = '';
            Object.keys(feature.properties).forEach((key) => {
              if (key === this.selected) {
                contentHTML += '<mark>';
              }
              contentHTML += `${key}: ${feature.properties[key]}`;
              if (key === this.selected) {
                contentHTML += '</mark>';
              }
              contentHTML += '<br />';
            });
            popupHTML.innerHTML = contentHTML;
            layer.bindPopup(popupHTML);
          },
          style: (feature) => ({
            color: this.scaleColor(feature.properties[this.selected]),
          }),
        });
        this.featureGroup.addLayer(geoJson);
      });
    },
  },
};
</script>

<style scoped>
  .map {
    width: 800px;
    height: 600px;
    margin-left: auto;
    margin-right: auto;
  }
  .legend-line {
    stroke-width: 4px;
  }
  li {
    list-style: none;
  }
</style>
