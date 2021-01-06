<template>
  <div id="app">
    <Toolbar />
    <md-card class="md-eleveation-24">
      <vue-plotly :data="data" :layout="layout" :options="options"/>
    </md-card>
    <PCAList :entries="listData"/>
    <md-snackbar :md-duration="5000" :md-active.sync="showSnackbar" md-persistent>
      <span>Retreiving list of images failed, due to: {{ error }}</span>
      <md-button class="md-primary" @click="showSnackbar = false">Ok :(</md-button>
    </md-snackbar>
  </div>
</template>

<script>
import Toolbar from './components/Toolbar.vue'
import VuePlotly from '@statnett/vue-plotly'
import PCAList from './components/PCAList.vue'

import ApiClient from './client/api_client.js'

const client = new ApiClient("http://127.0.0.1:5000")

export default {
  name: 'App',
  components: {
    Toolbar,
    VuePlotly,
    PCAList
  },
  data: function () {
    return {
      data: [],
      layout: {
        autosize: true,
        height: 500,
        margin: {
          l: 50,
          r: 50,
          b: 100,
          t: 100,
          pad: 4
        },
      },
      options: {},
      listData: [],
      showSnackbar: false,
      error: null,
    }
  },
  methods: {
    updateList() {
      client.getData().then((data) => {
        const predefined = {
          x: [], y: [], text: [], prediction: [], image: [],
          mode: 'markers',
          marker: {
            size: 12,
            line: {
            color: 'rgba(217, 217, 217, 0.14)',
            width: 0.5},
            opacity: 0.8},
          type: 'scatter',
          hovertemplate: 'Name:%{text}<br> Prediction:%{prediction}<br> Image:%{image}<br> x: %{x}<br> y: %{y}<br>',
          name: "Predefined"
        };
        const userDefined = {
          x: [], y: [], text: [], prediction: [], image: [],
          mode: 'markers',
          marker: {
            color: 'rgb(127, 127, 127)',
            size: 12,
            symbol: 'circle',
            line: {
            color: 'rgb(204, 204, 204)',
            width: 1},
            opacity: 0.8},
          type: 'scatter',
          hovertemplate: 'Name: %{text}<br> Prediction: %{prediction}<br> Image: %{image}<br> x: %{x}<br> y: %{y}<br>',
          name: "User Defined"
        };

        data.forEach(element => {
          if (element.predefined) {
            predefined.x.push(element.x);
            predefined.y.push(element.x);
            predefined.image.push("http://127.0.0.1:5000" +element.url);
            predefined.prediction.push(element.prediction);
            predefined.text.push(element.name)
            //predefined.z.push(element.z);
          } else {
            userDefined.x.push(element.x);
            userDefined.y.push(element.x);
            userDefined.image.push("http://127.0.0.1:5000" +element.url);
            userDefined.prediction.push(element.prediction);
            userDefined.text.push(element.name)
            //userDefined.z.push(element.z);
          }
        });

        this.data = [predefined, userDefined];
        this.listData = data.map(e => {
          if (e.predefined) {
            e.icon = "dns"
          } else {
            e.icon = "account_box"
          }
          e.url = "http://127.0.0.1:5000" + e.url

          return e
        });
      }).catch(e => {
        this.error = e;
        this.showSnackbar = true;
      });
    },
    uploadImage(file, name){
      return client.uploadFile(file, name);
    }
  },
  mounted() {
    this.updateList()
  },
}
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Material+Icons");
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
