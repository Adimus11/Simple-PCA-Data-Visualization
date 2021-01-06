<template>
  <div>
        <md-card class="md-elevation-12" v-for="entry in entries" :key="entry.id">
            <md-card-header>
                <md-card-header-text>
                    <div class="md-title">{{ entry.name }}</div>
                    <div class="md-subhead">{{ entry.prediction }}</div>
                </md-card-header-text>

                <md-card-media>
                <img :src=entry.url alt="Image of object">
                </md-card-media>
            </md-card-header>

            PCA 1st component: {{ entry.x }}<br>
            PCA 2st component: {{ entry.y }}<br>
            PCA 3st component: {{ entry.z }}<br>

            <md-card-actions>
                <md-button class="md-icon-button">
                    <md-icon>{{ entry.icon }}</md-icon>
                </md-button>
            </md-card-actions>
        </md-card>
  </div>
</template>

<style lang="scss" scoped>
  .md-card {
    width: 320px;
    margin: 12px;
    display: inline-block;
    vertical-align: top;
  }
</style>

<script>
export default {
  name: 'PCAList',
  props: {
    entries: Array
  }
}
</script>
