import L from 'leaflet';

import { mapBoxKey } from '@/assets/keys';

const options = { tileSize: 512, maxZoom: 18, zoomOffset: -1 };

export default (attribution = '') => ({
  dark: L.tileLayer(
    `https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/{z}/{x}/{y}@2x?access_token=${mapBoxKey}`,
    {
      attribution: `${attribution}&copy; <a href="https://www.mapbox.com/feedback/">Mapbox</a>
                  &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>`,
      ...options,
    },
  ),
  light: L.tileLayer(
    `https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}@2x?access_token=${mapBoxKey}`,
    {
      attribution: `${attribution}&copy; <a href="https://www.mapbox.com/feedback/">Mapbox</a>
                  &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>`,
      ...options,
    },
  ),
  satellite: L.tileLayer(
    `https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/tiles/{z}/{x}/{y}@2x?access_token=${mapBoxKey}`,
    {
      attribution: `${attribution}&copy; <a href="https://www.mapbox.com/feedback/">Mapbox</a>
                  &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>`,
      ...options,
    },
  ),
});
