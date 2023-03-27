const sensor={template: `
<div>
<table class = "table table-stripped">
<thead>
    <tr>
        <th>
            Date
        </th>
        <th>
            Depth
        </th>
        <th>
            Site
        </th>
        <th>
            Moisture
        </th>
    </tr>
</thead>
<tbody>
    <tr v-for ="data in sensorData">
        <td> {{data.Date}} </td>
        <td> {{data.Depth}} </td>
        <td> {{data.Site}} </td>
        <td> {{data.Value}} </td>
    </tr>
</tbody>
</thead>
</table>
</div>
`,
data() {
    return{
        sensorData:[]
    }
},
methods:{
    refreshData(){
        axios.get("http://127.0.0.1:8000/viewsensordata")
        .then((response) => {
            this.sensorData = response.data;
        });

    }
},
mounted:function(){
    this.refreshData();
}

}