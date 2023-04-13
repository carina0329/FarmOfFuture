<template>
  <div style="display: flex; flex-direction: column; align-items: center;">
    <canvas id="sensor" style="height: 400px;"></canvas>
    <div v-if="loading" style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
      <p>Loading...</p>
    </div>
    <div v-if="showAlert" class="alert" :style="{ backgroundColor: alertBgColor, color: alertTextColor, padding: alertPadding, marginBottom: alertMarginBottom }">
      {{ alertMessage }}
      <button @click="showAlert = false">Close</button>
    </div>
    <div v-else style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
      <input type="text" id="inputBox" v-model="date_1" placeholder="Start Date" style="margin-right: 1rem; padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px;">
      <input type="text" id="inputBox2" v-model="date_2" placeholder="End Date" style="margin-right: 1rem; padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px;">
      <select v-model="depth" style="margin-right: 1rem; padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px;">
        <option disabled value="">Depth</option>
        <option v-for="depth in depth_list" :value="depth" :key="depth">{{ depth }}</option>
      </select>
      <select v-model="site" style="margin-right: 1rem; padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px;">
        <option disabled value="">Site</option>
        <option v-for="site in site_list" :value="site" :key="site">{{ site }}</option>
      </select>
      <select v-model="plot" style="margin-right: 1rem; padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px;">
        <option disabled value="">Plot</option>
        <option v-for="plot in plot_list" :value="plot" :key="plot">{{ plot }}</option>
      </select>
      <button @click="renderLineGraph(date_1, date_2, site, plot, depth)" style="background-color: #4CAF50; color: white; padding: 0.5rem; border: none; border-radius: 5px;">Get Soil Data</button>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import axios from 'axios';
export default {
  data() {
    return {
      depth_list: [],
      date_to_depthToVal: {},
      date_list: [],
      plot_list: [],
      site_list: [],
      date_1: null,
      date_2: null,
      depth: null,
      chartObj: null,
      loading: true,
      site: null,
      plot: null,
      showAlert: false,
      alertMessage: "",
      alertBgColor: "#f44336",
      alertTextColor: "white",
      alertPadding: "10px",
      alertMarginBottom: "15px",
    }
  },
  methods: {
    callAlert(msg) {
      this.alertMessage = msg;
      this.showAlert = true;
    },
    async initializeLineGraph(){
        this.loading = true;
        await this.refreshData();
        // get the latest date available
        const last10 = this.date_list.slice(-10)
        this.renderLineGraph(last10[0], last10[9], "energyFarm", "MaizeControl", 20)
        this.loading = false;
    },
    renderLineGraph(date_1, date_2, site, plot, depth){
        // label
        // let date_list = []
        // let depthToVal = {}
        let label_lst = []
        for(let idx in this.date_list) {
            if(this.date_list[idx] <= date_2 && this.date_list[idx] >= date_1) {
                label_lst.push(this.date_list[idx]);
            }
        }
        if(label_lst.length == 0){
            this.callAlert("No Available Dates!")
        }
        // construct dataset to display
        var dataset_sliced = {}
        var value_array_render = []
        for(let label in label_lst){
            // console.log(label_lst[label])
            if(label_lst[label] in this.date_to_depthToVal) {
                // console.log(this.date_to_depthToVal[label_lst[label]])
                dataset_sliced = this.date_to_depthToVal[label_lst[label]]
            }
            else{
                this.callAlert("No Available Dates in the database!")
            }
            if(site in dataset_sliced && (plot in dataset_sliced[site]) && (depth in dataset_sliced[site][plot])){
                value_array_render.push(dataset_sliced[site][plot][depth][0])
            }
            else {
                this.callAlert("No data that matches the filters! Try again")
            }
        }
        console.log(value_array_render)
        const data = {
            labels: label_lst,
            datasets: [
                {
                    label: depth,
                    data: value_array_render,
                    yAxisID: 'y',
                },
            ]
        };
        const config = {
            type: 'line',
            data: data,
            options: {
              responsive: true,
              interaction: {
                mode: 'index',
                intersect: false,
              },
              stacked: false,
              plugins: {
                title: {
                  display: true,
                  text: 'Soil Moisture in the specified date range and depth'
                }
              },
              scales: {
                y: {
                  type: 'linear',
                  display: true,
                  position: 'left',
                },
              }
            },

        };
        let canvas = document.getElementById('sensor');
        console.log(canvas)
        if(this.chartObj) {
            this.chartObj.destroy();
            console.log("Destroyed Successfully")
        }
        this.chartObj = new Chart(
            canvas,
            config,
        )
    },
    async refreshData(){
        await axios.get("http://127.0.0.1:8000/viewsensordata")
        .then((response) => {
            var sensorData = response.data;
            // console.log(this.sensorData);
            console.log(sensorData.length);
            if(sensorData.length <= 0) {
                throw new Error('Sensor Data is none!');
            }
            for (let i = 0; i < sensorData.length; ++i) {
                let date = sensorData[i].Date
                if(!(date in this.date_to_depthToVal)) {
                    this.date_list.push(date);
                    this.date_to_depthToVal[date] = {}
                    // depthToVal_tmp = {}
                }
                let site = sensorData[i].Site
                let plot = sensorData[i].Plot
                let value = sensorData[i].Value
                // console.log(value);
                let depth = sensorData[i].Depth;
                // console.log(depth);
                if(this.site_list.indexOf(site) === -1) {
                    console.log(site)
                    this.site_list.push(site);
                }
                if(this.plot_list.indexOf(sensorData[i].Plot) === -1) {
                    this.plot_list.push(sensorData[i].Plot);
                }
                if(this.depth_list.indexOf(sensorData[i].Depth) === -1) {
                    this.depth_list.push(sensorData[i].Depth);
                }
                
                if(!(site in this.date_to_depthToVal[date])) {
                    this.date_to_depthToVal[date][site] = {};
                }
                if(!(plot in this.date_to_depthToVal[date][site])) {
                    this.date_to_depthToVal[date][site][plot] = {};
                }
                if(depth in this.date_to_depthToVal[date]){
                    this.date_to_depthToVal[date][site][plot][depth].push(value);
                }
                else{
                    this.date_to_depthToVal[date][site][plot][depth] = [value];
                }
                // this.date_to_depthToVal[date] = depthToVal_tmp;
            }
        })
    },
  },
   mounted:function(){
        this.initializeLineGraph()
   }
}
</script>
<style>
@media only screen and (max-width: 768px) {
  input[type="text"], select {
    width: 100%;
    margin-bottom: 1rem;
  }
}
</style>