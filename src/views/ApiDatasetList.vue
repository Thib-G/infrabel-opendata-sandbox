<template>
  <div>
    <p>Retrieve dataset list from API</p>
    <p><tt>https://opendata.infrabel.be/api/datasets/1.0/search?start={{ start }}</tt></p>
    <div v-if="datasets">
      <p><b>{{ datasets.nhits }}</b> datasets,
        showing <b>{{ datasets.parameters.start + 1 }}</b> &ndash;
        <b>{{ datasets.parameters.start + datasets.datasets.length }}</b>
        / <b>{{ datasets.nhits }}</b></p>
        <p>
          <a href v-if="datasets.parameters.start > 0" @click.prevent="start -= 10">prev</a>&nbsp;
          <a href v-if="datasets.parameters.start + datasets.datasets.length
            < datasets.nhits" @click.prevent="start += 10">next</a>
        </p>
      <table>
        <thead>
          <tr>
            <th class="right">Dataset ID&nbsp;&nbsp;</th>
            <th class="left">&nbsp;&nbsp;Title</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in datasets.datasets" :key="d.datasetid">
            <td class="right"><a :href="`https://opendata.infrabel.be/explore/dataset/${d.datasetid}`"
              target="_blank">{{ d.datasetid }}</a></td>
            <td class="left">{{ d.metas.title }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import InfrabelService from '@/services/infrabel-service';

export default {
  data() {
    return {
      infrabelService: InfrabelService,
      start: 0,
      datasets: undefined,
    };
  },
  created() {
    this.getDatasets();
  },
  watch: {
    start() {
      this.getDatasets();
    },
  },
  methods: {
    getDatasets() {
      this.infrabelService.getDatasets(this.start).then((data) => {
        this.datasets = data;
      });
    },
  },
};
</script>

<style scoped>
  table {
    margin-left: auto;
    margin-right: auto;
  }
  .left {
    text-align: left;
  }
  .right {
    text-align: right;
  }
</style>
