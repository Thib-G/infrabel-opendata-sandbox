<template>
  <div>
    <p>
      This visualisation animates the top longest main tracks.
      <br>Click <a
        href
        @click.prevent="animate"
        @keydown.prevent="animate"
      >Play</a>.
    </p>
    <LengthOfTracksGeo
      v-if="geojson && regions"
      :geojson="geojson"
      :regions="regions"
      ref="geo"
    />
    <div>
      <button @click="animate">
        Play
      </button>
    </div>
    <h3>Sources</h3>
    <p>
      Infrabel Open Data: &laquo;&nbsp;<a
        href="https://opendata.infrabel.be/explore/dataset/geovoies/"
        target="_blank"
      >Liste
        et position géographique des voies principales</a>&nbsp;&raquo;.
    </p>
    <p>
      The dataset was simplified using QGIS with the Douglas-Peucker
      algorithm and a precision of 50m.
    </p>
    <p>
      Atlas de Belgique: <a
        href="http://www.atlas-belgique.be/cms2/index.php?page=cartodata_fr"
        target="_blank"
      >régions</a>.
    </p>
  </div>
</template>

<script>
// @ is an alias to /src
import InfrabelService from '@/services/infrabel-service';
import LengthOfTracksGeo from '@/components/LengthOfTracksGeo.vue';

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
    LengthOfTracksGeo,
  },
};
</script>
