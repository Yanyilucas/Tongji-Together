<template>
  <template v-if="userInfo">
    <nut-grid :column-num="3" :border="false">
    <nut-grid-item ></nut-grid-item>
    <nut-grid-item >
     <nut-avatar size="large" custom-color="#ffffff" bg-color="#FA2C19">
        {{ userInfo.Name?.[0] || '' }}
      </nut-avatar>
    </nut-grid-item>
    <nut-grid-item></nut-grid-item>
    </nut-grid>

    <!-- 日历预约内容,只显示最近的 出行 和 拼车 -->
    <view style="text-align: center; font-size: 16px; font-weight: bold;">
      {{ userInfo.Name || '用户' }}，欢迎回来！
    </view>

    <!-- 🔽 新增：最近的出行模块(仅车主)
    
    <view style="margin: 30rpx 20rpx 10rpx; font-size: 16px; font-weight: bold;" v-if="userInfo.isDriver">
      最近的出行
    </view>
    <view style="padding: 0 20rpx;" v-if="userInfo.isDriver">
      <nut-empty description="最近没有出行计划哦" />
    </view> -->

    <!-- 🔽 新增：最近的拼车模块 -->
    <view style="margin: 30rpx 20rpx 10rpx; font-size: 16px; font-weight: bold;">
      最近的拼车
    </view>
     <view style="padding: 0 20rpx;" v-if=" myTrips.length > 0">
      <TripCard v-for="item in myTrips" :key="item.PostingID" :item="item" :showMap="false"/>
    </view>
    <view style="padding: 0 20rpx;" v-else>
      <nut-empty  description="最近没有拼车计划哦" />
    </view>


    <nut-cell-group>
      <nut-cell>
        <nut-button type="primary" block @click="showBottom = true" v-if="!userInfo.isDriver"> 成为车主</nut-button>
        <nut-button type="primary" block  v-else @click="handleUnRegisterDriver" plain>注销车主</nut-button>
      </nut-cell>
      <nut-cell>
         <nut-button type="primary" block @click="toLogout" plain> 退出登录 </nut-button>
      </nut-cell>
    </nut-cell-group>
    <nut-popup position="bottom" round :custom-style="{ height: '80%' }" v-model:visible="showBottom">
      <view style="padding: 20px">
        <text style="font-size: 16px; font-weight: bold; display: block; margin-top: 10px;">
          要成为顺风车车主，需要具备以下条件
        </text>

        <text style="font-size: 15px; font-weight: bold; display: block; margin-top: 10px;">一、符合基础驾驶条件</text>
        <text style="display: block;">1. 年龄：18-70周岁；</text>
        <text style="display: block;">2. 身体状况：健康；</text>
        <text style="display: block;">3. 驾龄：无驾龄限制；</text>
        <text style="display: block;">4. 驾驶证准驾车型：至少包含A1、A2、A3、B1、B2、C1、C2准驾车型的驾驶证。</text>

        <text style="font-size: 15px; font-weight: bold; display: block; margin-top: 10px;">二、无不良记录</text>
        <text style="display: block;">1. 无违法犯罪记录（含暴力犯罪记录、交通肇事犯罪记录、饮酒后驾驶记录、严重交通违法行为记录、吸毒记录）；</text>
        <text style="display: block;">2. 无其他严重不良记录；</text>
        <text style="display: block;">3. 未因涉嫌犯罪处于被调查、侦查等阶段或者被公安机关列入在逃人员名单的。</text>

        <text style="font-size: 15px; font-weight: bold; display: block; margin-top: 10px;">三、拥有满足条件的车辆</text>
        <text style="display: block;">1. 车辆条件：7座及以下车辆且车况良好；</text>
        <text style="display: block;">2. 车辆所有人：自有车辆或者获得车主本人许可，驾驶车辆必须为认证通过的车辆；</text>
        <text style="display: block;">3. 车龄（车辆注册日期）：15年以内；</text>
        <text style="display: block;">4. 车辆需按期年检，且有车辆保险齐全。</text>
      </view>
      <nut-cell >
    <nut-button type="primary" block @click="handleRegisterDriver">
      我已知悉,现在成为车主
    </nut-button>
    </nut-cell>
    </nut-popup>

   

  </template>

  <template v-else>
    <view class="avatar-wrapper">
      <nut-avatar size="large" bg-color="#FA2C19" custom-color="#ffffff">
        <nut-icon name="my" size="50"></nut-icon>
      </nut-avatar>
    </view>
    <nut-button type="primary" block @click="toLogin">
      登录/注册
    </nut-button>
  </template>
</template>

<script setup>
import { ref } from 'vue'
import { useRequest } from '@/api'
import { onShow } from '@dcloudio/uni-app'
import TripCard from '../index/TripCard.vue'
const { API_USERINFO_GET,API_REGISTER_DRIVER_POST,API_UNREGISTER_DRIVER_POST,API_MYTRIP_GET } = useRequest()

const showBottom = ref(false) 
const userInfo = ref(null)
const myTrips = ref([])

onShow(async () => {
  if (userInfo.value) {
    console.log('用户信息已存在，直接使用')
  }else{
    try {
      const res = await API_USERINFO_GET()
      console.log('用户已登录，信息为:', res)
      userInfo.value = res
    } catch (err) {
      console.warn('用户未登录或 token 无效')
      userInfo.value = null
    }
  }

  try{
  myTrips.value = await API_MYTRIP_GET()
  console.log('我的行程:', myTrips)
  }catch(err){
    console.error('获取我的行程失败:', err)
  }

})


function toLogin() {
  uni.navigateTo({ url: '/pages/user/login' })
}


function toLogout() {
  uni.clearStorageSync()
  userInfo.value = null  
}


async function handleRegisterDriver() {
  try {
    const res =await API_REGISTER_DRIVER_POST()
    uni.showToast({ title:res?.message || '申请成功', icon: 'success' })

    // 可选：刷新用户信息
    showBottom.value = false
    const resInfo = await API_USERINFO_GET()
    userInfo.value = resInfo
  } catch (err) {
    console.error('申请失败:', err)
    uni.showToast({ title: err?.message || '申请失败', icon: 'none' })
  }
}

// 处理注销车主逻辑
function handleUnRegisterDriver() {
  uni.showModal({
    title: '确认注销车主身份吗？',
    content: '注销后将无法使用车主相关功能',
    success: async (res) => {
      if (res.confirm) {
        try {
          // 调用注销车主接口
          await API_UNREGISTER_DRIVER_POST()
          uni.showToast({ title: '注销成功', icon: 'success' })
          userInfo.value.isDriver = false  // 更新用户信息
        } catch (err) {
          console.error('注销失败:', err)
          uni.showToast({ title: err?.message || '注销失败', icon: 'none' })
        }
      }
    }
  })
}

</script>
<style scoped>
.avatar-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20rpx 0;
}

.logo {
    height: 175rpx;
    width: 175rpx;
    margin-top: 100rpx;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 50rpx;
  }
</style>