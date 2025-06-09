<template>
  <view>
  


    <nut-button type="primary" @click="toLogin">登录</nut-button>
  </view>
</template>



<script setup>

const token = uni.getStorageSync('token')


//  跳转到登录界面
function toLogin() {
  uni.navigateTo({ url: '/pages/user/login' })
}
</script>