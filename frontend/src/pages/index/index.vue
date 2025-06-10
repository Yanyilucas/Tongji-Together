<template>
  <nut-cell>
    <image class="logo" src="/static/logo.png"></image>
  </nut-cell>
<nut-tabs v-model="state.tab1value">
  <nut-tab-pane title="🚶 人找车">
    <!-- 设置1️⃣-->
    
  </nut-tab-pane>
  <nut-tab-pane title="🚗 车找人">
    <!-- 发布行程 -->
    <TripForm />
  </nut-tab-pane>
</nut-tabs>



</template>
<script setup>
import { ref,reactive } from 'vue'
import TripForm from './TripForm.vue'

const state = reactive({
  tab1value: '0',
})

</script>



<style scoped>
.logo {
    height: 175rpx;
    width: 175rpx;
    margin-top: 100rpx;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 50rpx;
  }
.trip-map {
  width: 100vw;
  height: 60vh;
  margin-top: 20px;
  display: block;
}
</style>


