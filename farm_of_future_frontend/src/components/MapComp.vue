<template>
  <div>
    <div id="map-bx">
      <div id="map" style="height: 480px"></div>
    </div>
    <!-- <div>latest: {{ this.latestDate }}</div> -->
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
        <VDatePicker 
        v-model="date"
        :available-dates="available_dates"
        mask="YYYY-MM-DD">
        </VDatePicker>
      <button @click="setupLeafletMap(this.formattedDate)" style="background-color: #4CAF50; color: white; padding: 0.5rem; border: none; border-radius: 5px;">Get Satellite Data</button>
    </div>
  </div>
</template>

<script>
// import { ref } from 'vue';
import axios from 'axios'
import L from 'leaflet'
import 'leaflet-imageoverlay-rotated'
import 'leaflet/dist/leaflet.css'
import moment from 'moment';
export default {
  data() {
    return {
      date: moment().format("YYYY-MM-DD"),
      formattedDate: moment().format("YYYY-MM-DD"),
      topleftLat: null,
      topleftLng: null,
      bottomleftLat: null,
      bottomleftLng: null,
      toprightLat: null,
      toprightLng: null,
      imageUrl: null,
      mapInitialized: false,
      map: null,
      available_dates: null,
      latestDate: null
    }
  },
  watch: {
    date: function(newDate) {
      this.formattedDate = moment(newDate).format("YYYY-MM-DD");
    },
  },
  methods: {
    async get_available_dates() {
      console.log("get_available_dates invoked")
      var request_str = 'http://127.0.0.1:8000/getavailabledate/'
      await axios
        .get(request_str)
        .then(response => {
          this.available_dates = response.data
          console.log(this.available_dates)
        })
    },
    async get_data(date_input) {
      var request_str = 'http://127.0.0.1:8000/viewsatellitedata/' + date_input
      await axios
        .get(request_str)
        .then(response => {
          this.topleftLat = response.data[0].TopLeftLat
          this.topleftLng = response.data[0].TopLeftLng
          this.bottomleftLat = response.data[0].BottomLeftLat
          this.bottomleftLng = response.data[0].BottomLeftLng
          this.toprightLat = response.data[0].TopRightLat
          this.toprightLng = response.data[0].TopRightLng
          let path_list = response.data[0].ImageFilePath.split("/").slice(-3)
          this.imageUrl = './' + path_list[0] + "/" + path_list[1] + "/" + path_list[2]
          console.log(this.imageUrl)
          // this.imageUrl = '/satellite_data/image_files/20230308_155050_27_24cc_3B_AnalyticMS_SR_clip.png'
          
        })
    },
    initializeLeafletMap() {
      this.map = L.map('map').setView([40.113159, -88.211105], 10)
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map)
      this.mapInitialized = true
    },
    async setupLeafletMap(date) {
      console.log("Date is: ", date)
      // const formattedDate = moment(date.toISOString()).format('YYYY-MM-DD');
      // console.log("Date formatted is: ", formattedDate)
      await this.get_data(date)
      if (this.mapInitialized === true) {
        this.map.off()
        this.map.remove()
        this.mapInitialized = false
      }
      this.initializeLeafletMap();
      this.setImageOverlay();
    },
    setImageOverlay() {
      var topleft = L.latLng(this.topleftLat, this.topleftLng)
      var bottomleft = L.latLng(this.bottomleftLat, this.bottomleftLng)
      var topright = L.latLng(this.toprightLat, this.toprightLng)
      var imageUrl = this.imageUrl
      if (this.mapInitialized) {
        L.imageOverlay.rotated(imageUrl, topleft, topright, bottomleft).addTo(this.map)
      }
    }
  },
  async mounted() {
    await this.get_available_dates();
    // console.log("hjwvbcwrjhbw", this.available_dates)
    // let last_date_available =  moment.max(this.available_dates.map(date => moment(date))).format('YYYY-MM-DD');
    // console.log("gggggggg", last_date_available)
    var lst = JSON.parse(this.available_dates.replace(/'/g, '"') || '[]');
    this.available_dates = lst
    this.latestDate = moment.max(this.available_dates.map(date => moment(date))).format('YYYY-MM-DD');
    await this.setupLeafletMap(this.latestDate)
  }
}
</script>