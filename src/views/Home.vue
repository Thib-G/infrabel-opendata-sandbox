<template>
  <div class="home">
    <h3>This is a showcase of a few ways to reuse Infrabel’s open data</h3>
    <ul>
      <li v-for="route in $router.options.routes" :key="route.name">
        <router-link :to="route.path">{{ route.meta.descr }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'home',
};
</script>
