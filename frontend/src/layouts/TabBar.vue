<template>
  <nut-tabbar
    v-model="activeName"
    bottom
    safe-area-inset-bottom
    placeholder
    @tab-switch="onTabSwitch"
  >
    <nut-tabbar-item
      v-for="(item) in tabs"
      :key="item.name"
      :tab-title="item.title"
      :icon="item.icon"
      :name="item.name"
    />
  </nut-tabbar>
  

</template>

<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'

const activeName = ref('home')

const tabs = [
  { name: 'home', title: '首页', icon: 'home', path: '/pages/index/index' },
  { name: 'my', title: '我的', icon: 'my', path: '/pages/user/user' }
]

function onTabSwitch(item) {
  const matched = tabs.find(t => t.name === item.name)
  if (matched) {
    uni.switchTab({ url: matched.path })
  }
}

onShow(() => {
  const currentRoute = getCurrentPages().slice(-1)[0]?.route || ''
  const matched = tabs.find(tab => currentRoute === tab.path.replace(/^\//, ''))
  if (matched) {
    activeName.value = matched.name
  }
})
</script>