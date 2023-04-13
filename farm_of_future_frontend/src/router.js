import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import MapComp from './components/MapComp.vue'
import SensorComp from './components/SensorComp.vue'

Vue.use(Router)
const router=  new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/map',
      name: 'MapComp',
      component: MapComp
    },
    {
      path: '/sensor',
      name: 'SensorComp',
      component: SensorComp
    }
  ]
})
export default router;
