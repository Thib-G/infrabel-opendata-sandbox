<template>
  <div class="home">
    <h3>This is a showcase of some dataviz made with Infrabel’s open data</h3>
    <h1>Length of tracks</h1>
    <LengthOfTracks />
    <hr />
    <h1>Embedded map</h1>
    <EmbeddedMap />
    <hr />
    <h1>API Dataset List</h1>
    <ApiDatasetList />
    <hr />
  </div>
</template>

<script>
// @ is an alias to /src
import LengthOfTracks from '@/components/LengthOfTracks.vue';
import EmbeddedMap from '@/components/EmbeddedMap.vue';
import ApiDatasetList from '@/components/ApiDatasetList.vue';

export default {
  name: 'home',
  components: {
    LengthOfTracks,
    EmbeddedMap,
    ApiDatasetList,
  },
};
</script>
