<template>
  <nut-cell>
    <image class="logo" src="/static/logo.png"></image>
  </nut-cell>
<nut-tabs v-model="state.tab1value">
  <nut-tab-pane title="🚶 人找车">
    <!-- 设置1️ -->
  </nut-tab-pane>
  <nut-tab-pane title="🚗 车找人">
    <!-- 发布行程 -->

  </nut-tab-pane>
</nut-tabs>
</template>
<script lang="ts">
import { reactive } from 'vue';
export default {
  setup() {
    const state = reactive({
      tab1value: '0',
    });
    return { state };
  }
};
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
</style>

