import axios from 'axios';

export default {
  getGeoTracks() {
    return axios.get('json/geovoies-simpl.geojson').then((response) => {
      response.data.features.forEach((feature) => {
        feature.geometry.coordinates.forEach((coord) => {
          if (coord[0][0] > coord[coord.length - 1][0]) {
            coord.reverse();
          }
        });
        feature.geometry.coordinates.sort((a, b) => a[0][0] - b[0][0]);
      });
      return response.data;
    });
  },
  getRegions() {
    return axios.get('json/regions.geojson').then((response) => response.data);
  },
  getDatasets(start = 0) {
    return axios.get('https://opendata.infrabel.be/api/datasets/1.0/search', { params: { start } })
      .then((response) => response.data);
  },
  getLineSections() {
    return axios.get('https://opendata.infrabel.be/api/v2/catalog/datasets/lijnsecties/exports/geojson?rows=-1&timezone=UTC&pretty=false')
      .then((response) => response.data);
  },
};
