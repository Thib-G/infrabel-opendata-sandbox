module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? '/'
    : '/',
  transpileDependencies: [
    'd3-selection',
    'd3-geo',
    'd3-scale',
    'd3-transition',
    'd3-collection',
    'd3-array',
    'd3-scale-chromatic',
  ],
};
