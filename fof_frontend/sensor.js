const sensor={template: `
<div style="display: flex; flex-direction: column; align-items: center;">
  <canvas id="sensor"></canvas>
  <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
    <input type="text" id="inputBox" v-model="date_1" placeholder="Start Date" style="margin-right: 1rem; padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px;">
    <input type="text" id="inputBox2" v-model="date_2" placeholder="End Date" style="margin-right: 1rem; padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px;">
    <input type="text" id="inputBox3" v-model="depth" placeholder="Depth" style="margin-right: 1rem; padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px;">
    <button @click="renderLineGraph" style="background-color: #4CAF50; color: white; padding: 0.5rem; border: none; border-radius: 5px;">Get Soil Data</button>
  </div>
</div>

`,
data() {
    return{
        sensorData:[],
        depthToVal: {},
        date_list: [],
        date_1: null,
        date_2: null,
        depth: null,
        chartObj: null,
        canvas: null,
    }
},
methods:{
    renderLineGraph(){
        // label
        // let date_list = []
        // let depthToVal = {}
        label_lst = []
        console.log(this.date_2)
        console.log(this.date_list[0])
        for(idx in this.date_list) {
            if(this.date_list[idx] <= this.date_2 && this.date_list[idx] >= this.date_1) {
                label_lst.push(this.date_list[idx]);
            }
        }
        const data = {
            labels: label_lst,
            datasets: [
                {
                    label: this.depth,
                    data: this.depthToVal[this.depth],
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
    refreshData(){
        axios.get("http://127.0.0.1:8000/viewsensordata")
        .then((response) => {
            this.sensorData = response.data;
            // console.log(this.sensorData);
            console.log(this.sensorData.length);
            if(this.sensorData.length <= 0) {
                throw new Error('Sensor Data is none!');
            }
            for (let i = 0; i < this.sensorData.length; ++i) {
            date = this.sensorData[i].Date
            if(this.date_list.indexOf(date) === -1) {
                this.date_list.push(date);
            }
            let value = this.sensorData[i].Value
            // console.log(value);
            let depth = this.sensorData[i].Depth;
            // console.log(depth);
            if(depth in this.depthToVal){
                this.depthToVal[depth].push(value);
            }
            else{
                this.depthToVal[depth] = [value];
            }
        }       
    });
},
},
mounted:function(){
    this.refreshData();
}
}