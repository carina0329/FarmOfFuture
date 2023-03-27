const map={template: `
<div>
    <label for="inputBox">Enter Date: </label>
    <input type="text" id="inputBox" v-model="date">
    <button @click="setupLeafletMap"> Get Image</button>
    <div ref="mapContainer" class="map-container" style = "height: 480px"></div>
  </div>
`,
data (){
    return {
        date: null,
        topleftLat: null,
        topleftLng: null,
        bottomleftLat: null,
        bottomleftLng: null,
        toprightLat: null,
        toprightLng: null,
        imageUrl: null,
        mapInitialized: false,
        map: null,
    }
},
methods: {
    setupLeafletMap() {
    //   console.log("date"),
    //   console.log(this.date)
      var request_str = 'http://127.0.0.1:8000/viewsatellitedata/' + this.date
      axios
        .get(request_str)
        .then(response => (
            // console.log("response"),
            // console.log(response),
            this.topleftLat = response.data[0].TopLeftLat,
            // console.log(response.data[0].TopLeftLat),
            this.topleftLng = response.data[0].TopLeftLng,
            // console.log(response.data[0].TopLeftLng),
            this.bottomleftLat = response.data[0].BottomLeftLat,
            // console.log(response.data[0].BottomLeftLat),
            this.bottomleftLng = response.data[0].BottomLeftLng,
            // console.log(response.data[0].BottomLeftLng),
            this.toprightLat = response.data[0].TopRightLat,
            // console.log(response.data[0].TopRightLat),
            this.toprightLng = response.data[0].TopRightLng,
            // console.log(response.data[0].TopRightLng),
            this.imageUrl = '/' + response.data[0].ImageFilePath
        ))
      if (this.mapInitialized) {
        this.map.setView([40.113159, -88.211105], 10);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);
        console.log('Updating map for date:', this.date);
        this.setImageOverlay();
        return;
      }    
      this.map = L.map(this.$refs.mapContainer).setView([40.113159, -88.211105], 10); 
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);
      this.mapInitialized = true
      this.setImageOverlay();
    },
    setImageOverlay() {
      var topleft = L.latLng(this.topleftLat,this.topleftLng); // 0
      console.log(topleft)
      var bottomleft = L.latLng(this.bottomleftLat,this.bottomleftLng); // 1
      console.log(bottomleft)
    //   var bottomright = L.latLng(40.05280298472781,-87.82667198719467); // 2
      var topright = L.latLng(this.toprightLat,this.toprightLng); // 3
      console.log(topright)
      var imageUrl = this.imageUrl;
      console.log(imageUrl)
      L.imageOverlay.rotated(imageUrl, topleft, topright, bottomleft).addTo(this.map);
    }
},
computed: {},
mounted() {
    // axios
    //     .get('http://127.0.0.1:8000/viewsatellitedata/2023-02-19')
    //     .then(response => (this.info = response)) 
    // this.setupLeafletMap();
}
}
    