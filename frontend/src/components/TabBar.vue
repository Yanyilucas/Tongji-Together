<template>
  <view class="tabbar-wrapper">
    <nut-tabbar v-model="activeName" @tab-switch="tabSwitch">
      <nut-tabbar-item 
        v-for="(item,index) in List"
        :key="index" 
        :name="item.name" 
        :tab-title="item.title" 
        :icon="item.icon" />
    </nut-tabbar>
  </view>
</template>
<script>
   import{ ref } from 'vue';
  export default{
    setup() {
      const activeName = ref("category");
      const List = [
      {
        title: '首页',
        icon: 'home',
        name: 'home',
      },
      {
        title: '发现',
        icon: 'find',
        name: 'find',
      },
      {
        title: '我的',
        icon: 'my',
        name: 'my',
      },
    ]
      function tabSwitch(item, index) {
        console.log(item, index);
      }
      return {
        tabSwitch,
        List,
        activeName,
      };
    },
  }
</script>
<style scoped>
.tabbar-wrapper {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 999;
}
</style>