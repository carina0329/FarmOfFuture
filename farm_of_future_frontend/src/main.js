/* eslint-disable */
import { createApp } from 'vue'
import App from './App.vue'
import VCalendar from 'v-calendar'
import { createRouter, createWebHistory } from 'vue-router'
import 'v-calendar/style.css';
import HelloWorld from './components/HelloWorld.vue'
import MapComp from './components/MapComp.vue'
import SensorComp from './components/SensorComp.vue'

const routes = [
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
  const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes, // short for `routes: routes`
  })

const app = createApp(App)

// Use plugin with optional defaults
app.use(VCalendar)
app.use(router)
app.mount('#app')

