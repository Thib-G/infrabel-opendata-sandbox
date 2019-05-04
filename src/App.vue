<template>
  <div id="app">
    <div id="nav">
      <template v-for="(route, index) in activeRoutes">
        <span :key="route.name">
          <router-link :to="route.path">{{ route.meta.descr }}</router-link>
          <span
            v-if="index < $router.options.routes.length - 1"
            :key="route.name"> | </span>
        </span>
      </template>
    </div>
    <h1>{{ $route.meta.descr }}</h1>
    <router-view/>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  computed: {
    activeRoutes() {
      return this.$router.options.routes.filter(r => r.name !== 'home');
    },
  },
};
</script>


<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
