<template>
  <div>
    Show line sections with attributes
    <div class="map" ref="map">
    </div>
    <div>
      <select v-model="selected">
        <option v-for="p in propList" :key="p" :value="p">{{ p }}</option>
      </select>
    </div>
    <h3>Sources</h3>
    <p><a href="https://opendata.infrabel.be/explore/dataset/segmentatie-volgens-de-eigenschappen-van-de-infrastructuur-en-de-exploitatiemoge"
      target="_blank">Section de lignes</a></p>
  </div>
</template>

<script>
// @ is an alias to /src
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

import { mapBoxKey } from '@/assets/keys';
import InfrabelService from '@/services/infrabel-service';

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
      infrabelService: InfrabelService,
      zoom: 8,
      belgiumCenterLatLng: [50 + (38 / 60) + (28 / 3600), 4 + (40 / 60) + (5 / 3600)],
      basemaps: {
        dark: L.tileLayer(
          `https://api.mapbox.com/v4/mapbox.dark/{z}/{x}/{y}@2x.png?access_token=${mapBoxKey}`,
          {
            attribution: `&copy; <a href="https://www.mapbox.com/feedback/">Mapbox</a>
                        &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>`,
          },
        ),
        light: L.tileLayer(
          `https://api.mapbox.com/v4/mapbox.light/{z}/{x}/{y}@2x.png?access_token=${mapBoxKey}`,
          {
            attribution: `&copy; <a href="https://www.mapbox.com/feedback/">Mapbox</a>
                        &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>`,
          },
        ),
        streets: L.tileLayer(
          `https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}@2x.png?access_token=${mapBoxKey}`,
          {
            attribution: `&copy; <a href="https://www.mapbox.com/feedback/">Mapbox</a>
                        &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>`,
          },
        ),
        satellite: L.tileLayer(
          `https://api.mapbox.com/v4/mapbox.streets-satellite/{z}/{x}/{y}@2x.png?access_token=${mapBoxKey}`,
          {
            attribution: `&copy; <a href="https://www.mapbox.com/feedback/">Mapbox</a>
                        &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>`,
          },
        ),
      },
      selected: undefined,
      featureGroup: L.featureGroup(),
      lineSections: undefined,
    };
  },
  mounted() {
    this.initMap();
    this.getLineSections();
  },
  watch: {
    lineSections() {
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
      const geoJson = L.geoJson(this.lineSections, {
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
      });
      this.featureGroup.addLayer(geoJson);
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
</style>
