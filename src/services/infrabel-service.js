import axios from 'axios';

export default {
  getGeoTracks() {
    return axios.get('json/geovoies-simpl.geojson').then(response => response.data);
  },
  getRegions() {
    return axios.get('json/regions.geojson').then(response => response.data);
  },
  getDatasets(start = 0) {
    return axios.get('https://opendata.infrabel.be/api/datasets/1.0/search', { params: { start } })
      .then(response => response.data);
  },
};
