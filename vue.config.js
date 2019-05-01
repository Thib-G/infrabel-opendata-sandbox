module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? '/infrabel-opendata-sandbox/'
    : '/',
  transpileDependencies: [
    'd3-selection',
    'd3-geo',
    'd3-scale',
    'd3-transition',
  ],
};
