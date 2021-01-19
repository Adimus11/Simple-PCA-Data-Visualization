<template>
  <div id="app">
    <Toolbar />
    <div class="md-layout md-gutter">
      <div class="md-layout-item md-size-75">
        <md-card class="md-eleveation-24" style="margin: 25px; margin-left: 10px; margin-right:10px">
          <Plotly :data="data" :layout="layout" :display-mode-bar="false" ref="myPlot"></Plotly>
        </md-card>
      </div>
      <div class="md-layout-item md-size-25">
        <md-card class="md-elevation-12" style="margin: 25px; margin-left: 0px; margin-right:10px">
            <md-card-header>
                <md-card-header-text>
                    <div class="md-title">{{ selected.name }}</div>
                    <div class="md-subhead">{{ selected.prediction }}</div>
                </md-card-header-text>

                <md-card-media>
                <img v-if="selected.url" :src=selected.url alt="Image of object">
                </md-card-media>
            </md-card-header>

            PCA 1st component: {{ selected.x }}<br>
            PCA 2st component: {{ selected.y }}<br>
            PCA 3st component: {{ selected.z }}<br>

            <md-card-actions>
                <md-button class="md-icon-button">
                    <md-icon>{{ selected.icon }}</md-icon>
                </md-button>
            </md-card-actions>
        </md-card>
      </div>
    </div>
    <PCAList :entries="listData"/>
    <md-snackbar :md-duration="5000" :md-active.sync="showSnackbar" md-persistent>
      <span>Retreiving list of images failed, due to: {{ error }}</span>
      <md-button class="md-primary" @click="showSnackbar = false">Ok :(</md-button>
    </md-snackbar>
  </div>
</template>

<script>
import Toolbar from './components/Toolbar.vue'
import { Plotly } from 'vue-plotly'
import PCAList from './components/PCAList.vue'

import ApiClient from './client/api_client.js'

const client = new ApiClient("http://127.0.0.1:5000")

export default {
  name: 'App',
  components: {
    Toolbar,
    Plotly,
    PCAList
  },
  data: function () {
    return {
      selected: {
        name: "Hover Over Point",
        prediction: "In order to see details",
        url: false,
        x: 0, y: 0, z:0,
        icon: ""
      },
      data: [],
      layout: {
        autosize: true,
        height: 500,
        margin: {
          l: 10,
          r: 10,
          b: 10,
          t: 10,
          pad: 4
        },
      },
      listData: [],
      showSnackbar: false,
      error: null,
    }
  },
  methods: {
    updateList() {
      client.getData().then((data) => {
        const predefined = {
          x: [], y: [], z: [], text: [], prediction: [], image: [],
          mode: 'markers',
          marker: {
            size: 12,
            line: {
            color: 'rgba(217, 217, 217, 0.14)',
            width: 0.5},
            opacity: 0.8},
          type: 'scatter3d',
          hovertemplate: 'Name:%{text}<br> x: %{x}<br> y: %{y}<br> z: %{z}<br>',
          name: "Predefined"
        };
        const userDefined = {
          x: [], y: [], z: [], text: [], prediction: [], image: [],
          mode: 'markers',
          marker: {
            color: 'rgb(127, 127, 127)',
            size: 12,
            symbol: 'circle',
            line: {
            color: 'rgb(204, 204, 204)',
            width: 1},
            opacity: 0.8},
          type: 'scatter3d',
          hovertemplate: 'Name: %{text}<br> x: %{x}<br> y: %{y}<br> z: %{z}<br>',
          name: "User Defined"
        };

        data.forEach(element => {
          if (element.predefined) {
            predefined.x.push(element.x);
            predefined.y.push(element.y);
            predefined.z.push(element.z);
            predefined.image.push("http://127.0.0.1:5000" +element.url);
            predefined.prediction.push(element.prediction);
            predefined.text.push(element.name)
          } else {
            userDefined.x.push(element.x);
            userDefined.y.push(element.y);
            userDefined.z.push(element.z);
            userDefined.image.push("http://127.0.0.1:5000" +element.url);
            userDefined.prediction.push(element.prediction);
            userDefined.text.push(element.name)
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
    console.log(this.$refs.myPlot)
    this.$refs.myPlot.$on('hover', d => {
      const data = d.points[0];
      console.log(data);
      this.selected.x = data.x;
      this.selected.y = data.y;
      this.selected.z = data.z;
      this.selected.name = data.data.text[data.pointNumber];
      this.selected.prediction = data.data.prediction[data.pointNumber];
      this.selected.url = data.data.image[data.pointNumber];

      if (data.data.name === "Predefined") {
        this.selected.icon = "dns"
      } else {
        this.selected.icon = "account_box"
      }
    });
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
