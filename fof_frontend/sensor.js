const sensor={template: `
<div>
    <div style="position: relative;">
      <canvas id="sensor"></canvas>
      <div style="position: absolute; bottom: 2cm; left: 5cm; display: flex; align-items: center;">
        <input type="text" id="inputBox" v-model="date_1" placeholder="Start Date" style="margin-right: 10px;">
        <input type="text" id="inputBox2" v-model="date_2" placeholder="End Date" style="margin-right: 10px;">
        <input type="text" id="inputBox3" v-model="depth" placeholder="Depth" style="margin-right: 10px;">
        <button @click="renderLineGraph" style="background-color: #4CAF50; color: white;">Get Soil Data</button>
      </div>
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
            if(this.date_list[idx] < this.date_2) {
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
                  text: 'Soil Moisture in the specified depth by user'
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
        this.canvas = document.getElementById('sensor');
        console.log(this.canvas)
        if(this.chartObj) {
            this.chartObj.destroy();
        }
        this.chartObj = new Chart(
            this.canvas,
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