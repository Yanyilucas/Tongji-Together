<template>
  <view>
    <nut-button type="primary" @click="toLogin">登录 / 注册</nut-button>
  </view>
</template>

<script setup>
function toLogin() {
  uni.navigateTo({ url: '/pages/user/login' })
}
</script>