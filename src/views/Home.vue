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
