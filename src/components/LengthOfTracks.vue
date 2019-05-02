<template>
  <div>
    <p>This visualisation animates the top longest main tracks</p>
    <GeoTracksComponent
      v-if="geojson && regions"
      :geojson="geojson"
      :regions="regions"
      ref="geo"
    />
    <div>
      <button @click="animate()">Animate</button>
    </div>
    <h3>Sources</h3>
    <p>Infrabel Open Data: &laquo;&nbsp;<a href="https://opendata.infrabel.be/explore/dataset/geovoies/"
      target="_blank">Liste
      et position géographique des voies principales</a>&nbsp;&raquo;.</p>
    <p>The dataset was simplified using QGIS with the Douglas-Peucker
      algorithm and a precision of 1m.</p>
    <p>Atlas de Belgique: <a href="http://www.atlas-belgique.be/cms2/index.php?page=cartodata_fr"
      target="_blank">régions</a>.</p>
  </div>
</template>

<script>
// @ is an alias to /src
import InfrabelService from '@/services/infrabel-service';
import GeoTracksComponent from '@/components/LengthOfTracks/GeoTracksComponent.vue';

export default {
  data() {
    return {
      infrabelService: InfrabelService,
      geojson: undefined,
      regions: undefined,
    };
  },
  created() {
    this.getGeoTracks();
    this.getRegions();
  },
  methods: {
    getGeoTracks() {
      this.infrabelService.getGeoTracks().then((data) => {
        this.geojson = data;
      });
    },
    getRegions() {
      this.infrabelService.getRegions().then((data) => {
        this.regions = data;
      });
    },
    animate() {
      this.$refs.geo.animate();
    },
  },
  components: {
    GeoTracksComponent,
  },
};
</script>
