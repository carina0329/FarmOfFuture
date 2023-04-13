
<template>
  <!-- <SensorComp /> -->
  <MapComp />
</template>

<script>
/* eslint-disable */
import HelloWorld from './components/HelloWorld.vue'
import MapComp from './components/MapComp.vue'
import SensorComp from './components/SensorComp.vue'
export default {
  name: 'App',
  components: {
    HelloWorld,
    MapComp,
    SensorComp,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
