import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    meta: {
      descr: 'Home',
    },
    // component: Home,
    redirect: '/length-of-tracks',
  },
  {
    path: '/length-of-tracks',
    name: 'length-of-tracks',
    meta: {
      descr: 'Length of tracks',
    },
    component: () => import(/* webpackChunkName: "length-of-tracks" */ '@/views/LengthOfTracks.vue'),
  },
  {
    path: '/line-sections',
    name: 'line-sections',
    meta: {
      descr: 'Line sections map',
    },
    component: () => import(/* webpackChunkName: "line-sections" */ '@/views/LineSectionsMap.vue'),
  },
  {
    path: '/embedded-map',
    name: 'embedded-map',
    meta: {
      descr: 'Embedded map',
    },
    component: () => import(/* webpackChunkName: "embedded-map" */ '@/views/EmbeddedMap.vue'),
  },
  {
    path: '/dataset-list',
    name: 'dataset-list',
    meta: {
      descr: 'Dataset list from API',
    },
    component: () => import(/* webpackChunkName: "dataset-list" */ '@/views/ApiDatasetList.vue'),
  },
  {
    path: '/about',
    name: 'about',
    meta: {
      descr: 'About',
    },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/About.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
