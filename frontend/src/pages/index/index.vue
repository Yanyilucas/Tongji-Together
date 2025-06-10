<template>
  <!-- <view class="content">
    <image class="logo" src="/static/logo.png"></image> -->
    <nut-navbar>
      <nut-tabs v-model="tabValue" @click="changeTab">
        <nut-tab-pane title="车找人" />
        <nut-tab-pane title="人找车" />
      </nut-tabs>
    </nut-navbar>
    <view v-if="tabValue === 0" class="tab-content">
      <text class="tab-title">🚗 当前显示：车找人</text>
      <!-- 示例内容：车找人列表 -->
      <view class="item">车辆1 - 上海 → 杭州 - 2025/06/10 08:00</view>
      <view class="item">车辆2 - 北京 → 天津 - 2025/06/11 14:00</view>
    </view>
    <view v-else class="tab-content">
      <text class="tab-title">🧍 当前显示：人找车</text>
      <!-- 示例内容：人找车需求列表 -->
      <view class="item">用户A - 南京 → 苏州 - 2025/06/10 09:30</view>
      <view class="item">用户B - 深圳 → 广州 - 2025/06/12 16:00</view>
    </view>
  <!-- </view> -->
</template>

<script setup>
import { ref } from 'vue'
const tabValue = ref(0)

function changeTab(tab) {
  tabValue.value = tab.paneKey
  console.log('当前tab切换为:', tabValue.value)
}
</script>

<style lang="scss">
  .logo {
    height: 200rpx;
    width: 200rpx;
    margin-top: 100rpx;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 50rpx;
  }

  .tab-content {
    padding: 20rpx;
  }

  .tab-title {
    font-size: 36rpx;
    font-weight: bold;
    margin-bottom: 20rpx;
    text-align: center;
  }

  .item {
    background-color: #f5f5f5;
    padding: 20rpx;
    border-radius: 12rpx;
    margin-bottom: 16rpx;
  }
</style>
