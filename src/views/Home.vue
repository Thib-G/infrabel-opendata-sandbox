<template>
  <div class="home">
    <h1>Length of tracks</h1>
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
    <p>Atlas de Belgique: <a href="http://www.atlas-belgique.be/cms2/index.php?page=cartodata_fr"
      target="_blank">régions</a>.</p>
    <hr />
  </div>
</template>

<script>
// @ is an alias to /src
import InfrabelService from '@/services/infrabel-service';
import GeoTracksComponent from '@/components/GeoTracksComponent.vue';

export default {
  name: 'home',
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
