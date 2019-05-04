import { select, selectAll } from 'd3-selection';

import { geoPath, geoMercator, geoCentroid } from 'd3-geo';

import { scaleLinear, scaleSequential, scaleBand } from 'd3-scale';

import { transition } from 'd3-transition';

import { interpolateYlOrBr, schemeCategory10 } from 'd3-scale-chromatic';

export default {
  select,
  selectAll,
  geoPath,
  geoCentroid,
  geoMercator,
  scaleLinear,
  scaleSequential,
  scaleBand,
  transition,
  interpolateYlOrBr,
  schemeCategory10,
};
