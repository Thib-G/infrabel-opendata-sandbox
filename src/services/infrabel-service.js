import axios from 'axios';

export default {
  getGeoTracks() {
    return axios.get('json/geovoies-simpl.geojson').then(response => response.data);
  },
  getRegions() {
    return axios.get('json/regions.geojson').then(response => response.data);
  },
};
