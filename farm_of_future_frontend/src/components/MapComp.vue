<template>
  <div>
    <div id="map-bx">
      <div id="map" style="height: 480px"></div>
    </div>
    <div v-if="showAlert" class="alert" :style="{ backgroundColor: alertBgColor, color: alertTextColor, padding: alertPadding, marginBottom: alertMarginBottom }">
      {{ alertMessage }}
      <button @click="showAlert = false">Close</button>
    </div>
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
        <VDatePicker 
        v-model="date"
        :attributes="this.attrs"
        mask="YYYY-MM-DD">
        </VDatePicker>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
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
      latestDate: null,
      attrs: null,
      showAlert: false,
      alertMessage: "",
      alertBgColor: "#f44336",
      alertTextColor: "white",
      alertPadding: "10px",
      alertMarginBottom: "15px",
    }
  },
  watch: {
    date: function(newDate) {
      this.formattedDate = moment(newDate).format("YYYY-MM-DD");
      if(this.available_dates.indexOf(this.formattedDate) !== -1) {
        console.log("yes, available")
        this.setupLeafletMap(this.formattedDate);
      }
      else{
        console.log("no, unavailable", this.formattedDate)
        this.callAlert("No Satellite picture was taken on this date")
      }
    },
  },
  methods: {
    callAlert(msg) {
      this.alertMessage = msg;
      this.showAlert = true;
    },
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
          this.topleftLat = response.data.TopLeftLat
          this.topleftLng = response.data.TopLeftLng
          this.bottomleftLat = response.data.BottomLeftLat
          this.bottomleftLng = response.data.BottomLeftLng
          this.toprightLat = response.data.TopRightLat
          this.toprightLng = response.data.TopRightLng
          let path_list = response.data.ImageFilePath.split("/").slice(-3)
          this.imageUrl = './' + path_list[0] + "/" + path_list[1] + "/" + path_list[2]
          console.log(this.imageUrl)
          // this.imageUrl = '/satellite_data/image_files/20230308_155050_27_24cc_3B_AnalyticMS_SR_clip.png'
        })
    },
    initializeLeafletMap() {
      this.map = L.map('map').setView([40.0677565, -88.211625], 16);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map)
      this.mapInitialized = true
    },
    async setupLeafletMap(date) {
      console.log("Date is: ", date)
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
      var topleft_ = L.latLng(40.069036142012, -88.21403682638878)
      var topright_ = L.latLng(40.06912901675976, -88.20924301795053)
      var bottomleft_ = L.latLng(40.06539844811567, -88.21395591822947)
      var imageUrl = this.imageUrl
      if (this.mapInitialized) {
        L.imageOverlay.rotated(imageUrl, topleft_, topright_, bottomleft_, {opacity: 0.9}).addTo(this.map)
      }
      var bounds = [
          [40.069036142012, -88.21403682638878],
          [40.06912901675976, -88.20924301795053],
          [40.065460367934776, -88.20926324499034],
          [40.06539844811567, -88.21395591822947]
      ].map(function(coords) { return L.latLng(coords); });
      L.rectangle(bounds).addTo(this.map);
    }
  },
  async mounted() {
    await this.get_available_dates();
    var lst = JSON.parse(this.available_dates.replace(/'/g, '"') || '[]');
    this.available_dates = lst
    this.latestDate = moment.max(this.available_dates.map(date => moment(date))).format('YYYY-MM-DD');
    var tmp_lst = []
    for(let idx in this.available_dates){
      var dt = new Date(this.available_dates[idx])
      // TODO: need to add the time diff with gmt
      dt.setHours(dt.getHours() + 8)
      tmp_lst.push(dt)
    }
  
    console.log("latest date: ", this.latestDate)
    this.attrs = ref([
        {
          key: 'available',
          highlight: 'red',
          dates: tmp_lst,
          dot: true,
        },
      ]),
    await this.setupLeafletMap(this.latestDate)
  }
}
</script>