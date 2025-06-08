<template>
  <view class="layout">
    <slot /> <!-- 页面内容 -->
    <TabBar />
  </view>
</template>

<script setup>
import TabBar from '@/layouts/TabBar.vue'
</script>

<style scoped>
.layout {
  position: relative;
  min-height: 100vh;
  padding-bottom: 100rpx; /* 为 TabBar 留出空间 */
  box-sizing: border-box;
}
</style>