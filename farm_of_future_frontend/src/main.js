/* eslint-disable */
import { createApp } from 'vue'
import App from './App.vue'
import VCalendar from 'v-calendar'
import 'v-calendar/style.css'; 

const app = createApp(App)

// Use plugin with optional defaults
app.use(VCalendar)

app.mount('#app')

