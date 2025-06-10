<template>
  <view class="trip-map">
    <map
      :latitude="mapCenter.latitude"
      :longitude="mapCenter.longitude"
      :markers="markers"
      :include-points="includePoints"
      scale="14"
      style="width: 100%; height: 100%;"
      @markertap="handleMarkerTap"
    />
  </view>
</template>

<script setup >
import { ref, watch, computed } from 'vue'

// 定义props
const props = defineProps({
  fromAddress: {
    type: String,
    default: ''
  },
  toAddress: {
    type: String,
    default: ''
  },
  center: {
    type: Object,
    default: () => ({ latitude: 31.2304, longitude: 121.4737 }) // 默认上海
  }
})

// 定义事件
const emit = defineEmits(['location-change'])

// 地图中心点
const mapCenter = ref(props.center)

// 标记点数组
const markers = ref<any[]>([])

// 包含所有点的区域
const includePoints = computed(() => {
  return markers.value.map(marker => ({
    latitude: marker.latitude,
    longitude: marker.longitude
  }))
})

// 处理标记点点击事件
function handleMarkerTap(e: any) {
  const markerId = e.detail.markerId
  const marker = markers.value.find(m => m.id === markerId)
  if (marker) {
    uni.showToast({
      title: marker.title,
      icon: 'none'
    })
  }
}

// 地理编码函数
async function geocode(address: string, label: 'From' | 'To') {
  if (!address) return
  
  try {
    const res: any = await uni.request({
      url: 'https://apis.map.qq.com/ws/geocoder/v1/',
      method: 'GET',
      data: {
        address,
        key: 'KKBBZ-UU7YL-4ZXP4-MMMJ5-BC4Q5-ZTFVO'
      }
    })

    const data: any = res.data
    if (data?.status === 0) {
      const loc = data.result.location
      const marker = {
        id: label === 'From' ? 1 : 2,
        latitude: loc.lat,
        longitude: loc.lng,
        title: `${label === 'From' ? '出发地' : '目的地'}: ${address}`,
        iconPath: label === 'From' 
          ? '/static/from.png' 
          : '/static/to.png',
        width: 32,
        height: 32,
        callout: {
          content: label === 'From' ? '出发地' : '目的地',
          color: '#fff',
          bgColor: label === 'From' ? '#1989fa' : '#ff4d4f',
          padding: 10,
          borderRadius: 4,
          display: 'BYCLICK'
        }
      } as any

      // 更新标记点
      const existingIndex = markers.value.findIndex(m => m.id === marker.id)
      if (existingIndex >= 0) {
        markers.value[existingIndex] = marker
      } else {
        markers.value.push(marker)
      }
      
      // 更新地图中心点
      if (markers.value.length === 1) {
        mapCenter.value = { latitude: loc.lat, longitude: loc.lng }
      }
      
      // 触发事件通知父组件
      emit('location-change', {
        type: label.toLowerCase(),
        latitude: loc.lat,
        longitude: loc.lng,
        address
      })
    }
  } catch (err) {
    uni.showToast({ title: `${label} 地址无效`, icon: 'none' })
  }
}

// 监听出发地变化
watch(() => props.fromAddress, (val) => {
  geocode(val, 'From')
})

// 监听目的地变化
watch(() => props.toAddress, (val) => {
  geocode(val, 'To')
})

// 暴露方法（如果需要）
defineExpose({
  setCenter(lat: number, lng: number) {
    mapCenter.value = { latitude: lat, longitude: lng }
  }
})
</script>

<style scoped>
.trip-map {
  width: 100%;
  height: 60vh;
  margin-top: 20px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 适配小程序样式 */
/* #ifdef MP-WEIXIN */
.trip-map {
  height: 300px;
}
/* #endif */
</style>