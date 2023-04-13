
<template>
  <div>
    <div id="nav">
    <div class="nav-item-wrapper">
      <router-link to="/" class="nav-item nav-home">Home</router-link>
    </div>
    <div class="nav-item-wrapper">
      <router-link to="/map" class="nav-item nav-map">Map</router-link>
    </div>
    <div class="nav-item-wrapper">
      <router-link to="/sensor" class="nav-item nav-sensor">Sensor</router-link>
    </div>
  </div>
    <router-view/>
    <div>
      <component :is="currentPage"></component>
    </div>
  </div>
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
#nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #eee;
  padding: 10px;
}

.nav-item-wrapper {
  display: inline-block;
  margin: 0 10px;
  border: 2px solid #2196F3;
  border-radius: 5px;
}

.nav-item {
  display: block;
  padding: 5px 10px;
  border-radius: 5px;
  background-color: #fff;
  color: #333;
  text-decoration: none;
  transition: background-color 0.3s ease;
}
.nav-home {
  background-color: #2196F3;
  color: #fff;
}

.nav-map {
  background-color: #4CAF50;
  color: #fff;
}

.nav-sensor {
  background-color: #f44336;
  color: #fff;
}

.nav-item:hover {
  background-color: #ccc;
  cursor: pointer;
}

.nav-item:active {
  background-color: #999;
}
.nav-item:focus,
.nav-item:active {
  outline: none;
  border: none;
  background-color: #2196F3;
  color: #fff;
}
</style>