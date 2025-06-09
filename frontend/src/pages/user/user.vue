<template>
  <nut-button
    type="primary"
    block
    @click="toLogin"
  >
    登录/注册
  </nut-button>

</template>

<script setup>
import { ref } from 'vue'
import { useRequest } from '@/api'
import { onShow } from '@dcloudio/uni-app'
const { API_USERINFO_GET } = useRequest()

onShow(async () => {
  try {
    const res = await API_USERINFO_GET()
    console.log('用户已登录，信息为:', res)
    console.log('用户信息:', res)

  } catch (err) {
    console.warn('用户未登录或 token 无效')
  }
})



function toLogin() {
  uni.navigateTo({ url: '/pages/user/login' })
}
</script>