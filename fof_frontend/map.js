const map={template: `
<div>
    <div id="map-bx">
      <div id="map" style = "height: 480px"></div>
    </div>
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
      <input type="text" id="inputBox" v-model="date" placeholder="Enter Date" style="margin-right: 1rem; padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px;">
      <button @click="setupLeafletMap(this.date)" style="background-color: #4CAF50; color: white; padding: 0.5rem; border: none; border-radius: 5px;">Get Satellite Data</button>
    </div>
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
    async get_data(date_input){
      var request_str = 'http://127.0.0.1:8000/viewsatellitedata/' + date_input
      await axios
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
    },
    initializeLeafletMap(){
      const content = document.getElementById('map');
      console.log(content);
      this.map = L.map('map').setView([40.113159, -88.211105], 10); 
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);
      this.mapInitialized = true
    },

    async setupLeafletMap(date) {
    //   console.log("date"),
    //   console.log(this.date)
      await this.get_data(date)
      console.log(this.imageUrl)
      if (this.mapInitialized === true) {
        console.log(this.map)
        this.map.off();
        this.map.remove();
        this.mapInitialized = false;
      }
      this.initializeLeafletMap();
      this.setImageOverlay();
    },
    
    setImageOverlay() {
      var topleft = L.latLng(this.topleftLat,this.topleftLng); // 0
      console.log(topleft)
      var bottomleft = L.latLng(this.bottomleftLat,this.bottomleftLng); // 1
      console.log(bottomleft)
    //   var bottomright = L.latLng(40.05280298472781,-87.82667198719467); // 2
      var topright = L.latLng(this.toprightLat,this.toprightLng); // 3
      // console.log(topright)
      var imageUrl = this.imageUrl;
      // console.log(imageUrl)
      if(this.mapInitialized) {
        const content = document.getElementById('map');
        console.log(content);
        L.imageOverlay.rotated(imageUrl, topleft, topright, bottomleft).addTo(this.map);
      }
    }
},
computed: {},
mounted() {
  this.setupLeafletMap("2023-03-10");
}
}
    