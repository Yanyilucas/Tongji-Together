<template>
  <view class="trip-form-container">
    <!-- 地图容器区块 -->
    <view class="map-block">
      <!-- 区块标题 -->
      <view class="block-header">
        <text class="block-title">行程地图</text>
      </view>
      
      <!-- 位置输入区域 -->
      <view class="location-inputs">
        <view class="input-row">
          <nut-icon name="location" size="16" color="#1989fa"></nut-icon>
          <nut-input 
            v-model="postingFormAddrset.From" 
            placeholder="请输入出发地" 
            clearable
            @input="searchLocations('From')"
            @focus="showSuggestions('From')"
            @blur="hideSuggestions('From')"
          />
        </view>
        
        <view class="input-row">
          <nut-icon name="location" size="16" color="#ff4d4f"></nut-icon>
          <nut-input 
            v-model="postingFormAddrset.To" 
            placeholder="请输入目的地" 
            clearable
            @input="searchLocations('To')"
            @focus="showSuggestions('To')"
            @blur="hideSuggestions('To')"
          />
        </view>
      </view>
      
      <!-- 地点建议列表 -->
      <view class="suggestion-list" v-show="suggestionsVisible.From || suggestionsVisible.To">
        <view 
          v-for="(item, index) in activeSuggestions" 
          :key="index"
          class="suggestion-item"
          @click="selectSuggestion(item)"
        >
          <view class="suggestion-icon">
            <nut-icon :name="item.type === 'From' ? 'location' : 'flag'" size="14" :color="item.type === 'From' ? '#1989fa' : '#ff4d4f'"></nut-icon>
          </view>
          <view class="suggestion-content">
            <text class="suggestion-title">{{ item.title }}</text>
            <text class="suggestion-address">{{ item.address }}</text>
          </view>
        </view>
      </view>
      
      <!-- 地图容器 -->
      <view class="map-container">
        <map
          :latitude="mapCenter.latitude"
          :longitude="mapCenter.longitude"
          :markers="activeMarkers"
          :scale="zoomLevel"
          :polyline="polyline"
          class="full-map"
          @markertap="handleMarkerTap"
        />
      </view>
      
      <!-- 地图控制按钮 -->
      <view class="map-controls">
        <nut-button 
          type="primary" 
          size="small" 
          plain
          @click="zoomIn"
        >
           <template #icon>
          <nut-icon name="plus" size="14"></nut-icon>
           </template>
        </nut-button>
        <nut-button 
          type="default" 
          size="small" 
          plain
          @click="zoomOut"
        >
        <template #icon>
          <nut-icon name="minus" size="14"></nut-icon>
        </template>
        </nut-button>
        <nut-button 
          type="info" 
          size="small" 
          plain
          @click="clearMarkers"
        >
          <template #icon>
          <nut-icon name="del" size="14"></nut-icon>
          </template>
        </nut-button>
      </view>
      
      <!-- 调试信息 -->
      <view class="debug-info" v-if="showDebugInfo">
        <text>路径点数量: {{ polyline.length > 0 ? polyline[0].points.length : 0 }}</text>
        <text v-if="polyline.length > 0">起点: {{ polyline[0].points[0] ? `${polyline[0].points[0].latitude.toFixed(6)}, ${polyline[0].points[0].longitude.toFixed(6)}` : '无' }}</text>
        <text v-if="polyline.length > 0">终点: {{ polyline[0].points[polyline[0].points.length - 1] ? `${polyline[0].points[polyline[0].points.length - 1].latitude.toFixed(6)}, ${polyline[0].points[polyline[0].points.length - 1].longitude.toFixed(6)}` : '无' }}</text>
        <text>地图中心: {{ mapCenter.latitude.toFixed(6) }}, {{ mapCenter.longitude.toFixed(6) }}</text>
        <text>缩放级别: {{ zoomLevel }}</text>
      </view>
      
      <!-- 调试按钮 -->
      <view class="debug-toggle">
        <nut-button 
          type="default" 
          size="small" 
          @click="showDebugInfo = !showDebugInfo"
        >
          {{ showDebugInfo ? '隐藏调试信息' : '显示调试信息' }}
        </nut-button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'

// props/model

const modelValue = defineModel('modelValue', { type: Object })

// 地图相关逻辑
const mapCenter = ref({ latitude: 31.2304, longitude: 121.4737 })
const zoomLevel = ref(13)
const polyline = ref([])
const routePoints = ref([])
const showDebugInfo = ref(false) // 调试信息开关
const {API_TENCENT_MAP_SUGGESTION_GET, API_TENCENT_MAP_ROUTE_GET} = useRequest()
// 表单数据
const postingFormAddrset = reactive(modelValue.value)

// 使用单独的fromMark和toMark替代markers列表
const fromMark = ref(null)
const toMark = ref(null)

// 计算属性：合并两个标记为数组
const activeMarkers = computed(() => {
  const markers = []
  if (fromMark.value) markers.push(fromMark.value)
  if (toMark.value) markers.push(toMark.value)
  return markers
})

// 地点建议功能
const suggestions = reactive({
  From: [],
  To: []
})

const suggestionsVisible = reactive({
  From: false,
  To: false
})

const activeInput = ref('')

// 计算当前显示的建议列表
const activeSuggestions = computed(() => {
  if (activeInput.value === 'From') return suggestions.From
  if (activeInput.value === 'To') return suggestions.To
  return []
})

// 地图控制方法
function zoomIn() {
  if (zoomLevel.value < 20) zoomLevel.value += 1
}

function zoomOut() {
  if (zoomLevel.value > 3) zoomLevel.value -= 1
}

// 清空所有标记和路径
function clearMarkers() {
  fromMark.value = null
  toMark.value = null
  modelValue.value.From = ''
  modelValue.value.To = ''
  modelValue.value.FromLat = 0
  modelValue.value.FromLng = 0
  modelValue.value.ToLat = 0
  modelValue.value.ToLng = 0
  polyline.value = []
  routePoints.value = []
}

// 创建标记对象
function createMarker(location, label) {
  const isFrom = label === 'From'
  const markerColor = isFrom ? '#1989fa' : '#ff4d4f'
  
  return {
    id: isFrom ? 1 : 2,
    latitude: location.lat,
    longitude: location.lng,
    title: `${isFrom ? '出发地' : '目的地'}: ${location.title || location.address}`,
    color: markerColor,
    width: 24,
    height: 24,
    callout: {
      content: isFrom ? '出发地' : '目的地',
      color: '#fff',
      bgColor: markerColor,
      padding: 10,
      borderRadius: 4,
      display: 'BYCLICK'
    }
  }
}

// 更新地图中心点
function updateMapCenter() {
  if (fromMark.value && toMark.value) {
    // 两地中心点
    const centerLat = (fromMark.value.latitude + toMark.value.latitude) / 2
    const centerLng = (fromMark.value.longitude + toMark.value.longitude) / 2
    mapCenter.value = { latitude: centerLat, longitude: centerLng }
    
    // 自动调整缩放级别
    const latDiff = Math.abs(fromMark.value.latitude - toMark.value.latitude)
    const lngDiff = Math.abs(fromMark.value.longitude - toMark.value.longitude)
    const maxDiff = Math.max(latDiff, lngDiff)
    
    if (maxDiff < 0.01) zoomLevel.value = 15
    else if (maxDiff < 0.05) zoomLevel.value = 13
    else if (maxDiff < 0.1) zoomLevel.value = 11
    else zoomLevel.value = 10
  } else if (fromMark.value) {
    mapCenter.value = { 
      latitude: fromMark.value.latitude, 
      longitude: fromMark.value.longitude 
    }
    zoomLevel.value = 15
  } else if (toMark.value) {
    mapCenter.value = { 
      latitude: toMark.value.latitude, 
      longitude: toMark.value.longitude 
    }
    zoomLevel.value = 15
  }
}

// 添加标记点
function addMarker(location, label) {
  const marker = createMarker(location, label)
  
  // 设置对应的标记
  if (label === 'From') {
    fromMark.value = marker
    modelValue.value.FromLat = location.lat
    modelValue.value.FromLng = location.lng
    modelValue.value.From = location.title || location.address
  } else {
    toMark.value = marker
    modelValue.value.ToLat = location.lat
    modelValue.value.ToLng = location.lng
    modelValue.value.To = location.title || location.address
  }
  
  updateMapCenter()
}


// 路径规划API调用 - 修复参数错误版本
async function planRoute() {
  if (!fromMark.value || !toMark.value) return
  
  console.log('开始路径规划...')
  console.log('起点坐标:', fromMark.value.latitude, fromMark.value.longitude)
  console.log('终点坐标:', toMark.value.latitude, toMark.value.longitude)
  
  try {
    const from = `${fromMark.value.latitude},${fromMark.value.longitude}`
    const to = `${toMark.value.latitude},${toMark.value.longitude}`
    
    // 确保坐标精度（最多6位小数）
    const formatCoord = coord => {
      const [lat, lng] = coord.split(',').map(parseFloat)
      return `${lat.toFixed(6)},${lng.toFixed(6)}`
    }

    const res = await API_TENCENT_MAP_ROUTE_GET(
      formatCoord(from), 
      formatCoord(to)
    )
    
    console.log('路径规划API响应:', res)

    if (res.status === 0 && res.result?.routes?.[0]?.polyline?.length > 0) {
      const compressed = res.result.routes[0].polyline
      const points = []
      
      // 打印原始压缩数据前10项
      console.log('压缩polyline数组（前10个）:', compressed.slice(0, 10))
      
      // 第一个点是绝对坐标
      let lat = compressed[0]
      let lng = compressed[1]
      
      // 验证起点坐标是否合理
      if (!isValidCoordinate(lat, lng)) {
        console.warn('起点坐标异常，尝试校正')
        lat = fromMark.value.latitude
        lng = fromMark.value.longitude
      }
      
      points.push({ latitude: lat, longitude: lng })

      // 从第3个数开始解码（增量编码）
      for (let i = 2; i < compressed.length; i += 2) {
        // 增量单位是万分度，除以10000转换为实际度数
        const deltaLat = compressed[i] / 1000000
        const deltaLng = compressed[i + 1] / 1000000
        
        lat += deltaLat
        lng += deltaLng
        
        points.push({ latitude: lat, longitude: lng })
      }

      console.log('路径点数量:', points.length)
      console.log('路径起点:', points[0])
      console.log('路径终点:', points[points.length - 1])
      
      // 验证终点坐标与预期相符
      const expectedLat = toMark.value.latitude
      const expectedLng = toMark.value.longitude
      const actualLat = points[points.length - 1].latitude
      const actualLng = points[points.length - 1].longitude
      
      if (Math.abs(actualLat - expectedLat) > 0.01 || 
          Math.abs(actualLng - expectedLng) > 0.01) {
        console.warn('终点坐标校正：预期 vs 实际', 
          [expectedLat, expectedLng], [actualLat, actualLng])
        points[points.length - 1] = {
          latitude: expectedLat,
          longitude: expectedLng
        }
      }
      
      // 设置路径线（确保所有点在有效范围内）
      polyline.value = [{
        points: points.map(p => ({
          latitude: clampCoordinate(p.latitude, 'lat'),
          longitude: clampCoordinate(p.longitude, 'lng')
        })),
        color: '#1989fa',
        width: 6,
        arrowLine: true,
        borderColor: '#fff',
        borderWidth: 2
      }]
      
      // 更新地图视图以包含整个路径
      updateMapCenterForRoute(points)
    } else {
      console.error('API路径规划失败:', res.message || '未返回有效路径')
      uni.showToast({
        title: `路径规划失败: ${res.message || '未知错误'}`,
        icon: 'none'
      })
    }
  } catch (err) {
    console.error('路径规划调用失败:', err)
    uni.showToast({
      title: '路径规划服务出错，请稍后再试',
      icon: 'none'
    })
  }
}

// 辅助函数：验证坐标有效性
function isValidCoordinate(lat, lng) {
  return lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180
}

// 辅助函数：坐标钳制到合法范围
function clampCoordinate(value, type) {
  if (type === 'lat') {
    return Math.max(-90, Math.min(90, value))
  }
  return Math.max(-180, Math.min(180, value))
}
// 为路径更新地图中心点
function updateMapCenterForRoute(points) {
  if (!points || points.length === 0) return
  
  // 计算路径边界
  let minLat = points[0].latitude
  let maxLat = points[0].latitude
  let minLng = points[0].longitude
  let maxLng = points[0].longitude
  
  points.forEach(point => {
    if (point.latitude < minLat) minLat = point.latitude
    if (point.latitude > maxLat) maxLat = point.latitude
    if (point.longitude < minLng) minLng = point.longitude
    if (point.longitude > maxLng) maxLng = point.longitude
  })
  
  // 计算中心点
  const centerLat = (minLat + maxLat) / 2
  const centerLng = (minLng + maxLng) / 2
  
  mapCenter.value = {
    latitude: centerLat,
    longitude: centerLng
  }
  
  // 自动调整缩放级别（根据路径跨度）
  const latDiff = maxLat - minLat
  const lngDiff = maxLng - minLng
  const maxDiff = Math.max(latDiff, lngDiff)
  
  if (maxDiff < 0.005) zoomLevel.value = 16
  else if (maxDiff < 0.01) zoomLevel.value = 14
  else if (maxDiff < 0.05) zoomLevel.value = 12
  else if (maxDiff < 0.1) zoomLevel.value = 10
  else zoomLevel.value = 8
}

// 监听起点终点变化
watch(
  () => [fromMark.value, toMark.value], 
  () => {
    if (fromMark.value && toMark.value) {
      planRoute()
    } else {
      polyline.value = []
    }
  },
  { deep: true }
)

// 地点搜索函数
async function searchLocations(type) {
  const keyword = postingFormAddrset[type]
  if (!keyword) {
    suggestions[type] = []
    return
  }
  
  try {
    const res = await API_TENCENT_MAP_SUGGESTION_GET(keyword)
    
    if (res.status === 0 && res.data) {
      suggestions[type] = res.data.map(item => ({
        title: item.title,
        address: item.address,
        lat: item.location.lat,
        lng: item.location.lng,
        type
      }))
    } else {
      throw new Error(`API错误: ${res.message || '未知错误'}`)
    }
  } catch (err) {
    console.error('位置搜索失败:', err)
  }
}

// 显示建议列表
function showSuggestions(type) {
  suggestionsVisible[type] = true
  activeInput.value = type
  if (postingFormAddrset[type]) {
    searchLocations(type)
  }
}

// 隐藏建议列表
function hideSuggestions(type) {
  setTimeout(() => {
    suggestionsVisible[type] = false
  }, 200)
}

// 选择建议项
function selectSuggestion(item) {
  suggestionsVisible[item.type] = false
  activeInput.value = ''
  
  addMarker({
    lat: item.lat,
    lng: item.lng,
    title: item.title,
    address: item.address
  }, item.type)
}

// 处理标记点点击
function handleMarkerTap(e) {
  const marker = activeMarkers.value.find(m => m.id === e.detail.markerId)
  if (marker) {
    uni.showToast({
      title: marker.title,
      icon: 'none'
    })
  }
}

// 组件挂载时初始化地图
onMounted(() => {
  // 初始设置空白地图
  fromMark.value = null
  toMark.value = null
})
</script>

<style scoped>
.trip-form-container {
  padding: 16px;
}

/* 地图区块样式 */
.map-block {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e8e8e8;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 24px;
  transition: all 0.3s ease;
}

.map-block:hover {
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* 区块头部 */
.block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
  background: linear-gradient(to right, #f9fbfd, #fff);
}

.block-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  position: relative;
  padding-left: 10px;
}

.block-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 16px;
  background: #1989fa;
  border-radius: 2px;
}

/* 位置输入区 */
.location-inputs {
  padding: 16px 20px 8px;
  border-bottom: 1px solid #f5f5f5;
}

.input-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  position: relative;
  gap: 10px;
}

.input-row .nut-icon {
  flex-shrink: 0;
  margin-right: 8px;
}

/* 地点建议列表 */
.suggestion-list {
  max-height: 250px;
  overflow-y: auto;
  background: #fff;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  z-index: 10;
}

.suggestion-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f5f5f5;
  transition: all 0.2s;
  cursor: pointer;
}

.suggestion-item:active {
  background-color: #f5f7fa;
}

.suggestion-icon {
  margin-right: 12px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #f0f8ff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.suggestion-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.suggestion-title {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.suggestion-address {
  font-size: 12px;
  color: #666;
}

/* 地图容器 */
.map-container {
  position: relative;
  width: 100%;
  height: 300px;
  overflow: hidden;
  background: #f9fbfd;
}

.full-map {
  position: absolute;
  width: 110%;
  height: 110%;
  top: -5%;
  left: -5%;
  z-index: 0;
}

/* 地图控制按钮 */
.map-controls {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.9);
  border-top: 1px solid #f5f5f5;
}

/* 调试信息 */
.debug-info {
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-top: 1px solid #e8e8e8;
  font-size: 12px;
  color: #666;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.debug-toggle {
  padding: 8px 16px;
  border-top: 1px solid #f5f5f5;
  display: flex;
  justify-content: center;
}

/* 响应式调整 */
@media (min-width: 768px) {
  .map-container {
    height: 360px;
  }
  
  .map-block {
    margin-bottom: 32px;
  }
}

/* 小程序适配 */
/* #ifdef MP-WEIXIN */
.map-container {
  height: 280px;
}

.full-map {
  width: 120%;
  height: 120%;
  top: -10%;
  left: -10%;
}
/* #endif */
</style>