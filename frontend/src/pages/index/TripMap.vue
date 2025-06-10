<template>
  <view class="trip-form-container">
    <!-- 地图容器区块 -->
    <view class="map-block">
      <!-- 区块标题 -->
      <view class="block-header">
        <text class="block-title">行程地图</text>
        <view class="block-actions" @click="centerToShanghai">
          <nut-icon name="location" size="16" color="#1989fa"></nut-icon>
          <text class="action-text">回到中心</text>
        </view>
      </view>
      
      <!-- 位置输入区域 -->
      <view class="location-inputs">
        <view class="input-row">
          <nut-icon name="location" size="16" color="#1989fa"></nut-icon>
          <nut-input 
            v-model="postingForm.From" 
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
            v-model="postingForm.To" 
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
          :markers="markers"
          :scale="zoomLevel"
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
          <nut-icon name="plus" size="14"></nut-icon>
        </nut-button>
        <nut-button 
          type="default" 
          size="small" 
          plain
          @click="zoomOut"
        >
          <nut-icon name="minus" size="14"></nut-icon>
        </nut-button>
        <nut-button 
          type="info" 
          size="small" 
          plain
          @click="clearMarkers"
        >
          <nut-icon name="del" size="14"></nut-icon>
        </nut-button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
const { API_TENCENT_MAP_SUGGESTION_GET } = useRequest()
// 地图相关逻辑
const mapCenter = ref({ latitude: 31.2304, longitude: 121.4737 }) // 上海市中心
const markers = ref([])
const zoomLevel = ref(13) // 默认缩放级别

// 表单数据
const postingForm = reactive({
  From: '',
  To: '',
  FromLat: 0,
  FromLng: 0,
  ToLat: 0,
  ToLng: 0,
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

const activeInput = ref('') // 当前活跃的输入框类型 ('From' 或 'To')

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

function centerToShanghai() {
  mapCenter.value = { latitude: 31.2304, longitude: 121.4737 }
  zoomLevel.value = 13
}

function clearMarkers() {
  markers.value = []
  postingForm.From = ''
  postingForm.To = ''
  postingForm.FromLat = 0
  postingForm.FromLng = 0
  postingForm.ToLat = 0
  postingForm.ToLng = 0
}

// 添加标记点
function addMarker(location, label) {
  const isFrom = label === 'From'
  const markerColor = isFrom ? '#1989fa' : '#ff4d4f'
  
  const marker = {
    id: isFrom ? 1 : 2,
    latitude: location.lat,
    longitude: location.lng,
    title: `${isFrom ? '出发地' : '目的地'}: ${location.title || location.address}`,
    // 使用默认标记并通过color属性设置颜色
    color: isFrom ? '#1989FA' : '#FF4D4F', // 蓝色表示出发地，红色表示目的地
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
  
  // 更新或添加标记点
  const existingIndex = markers.value.findIndex(m => m.id === marker.id)
  if (existingIndex >= 0) {
    markers.value[existingIndex] = marker
  } else {
    markers.value.push(marker)
  }
  
  // 更新表单中的位置信息
  if (isFrom) {
    postingForm.FromLat = location.lat
    postingForm.FromLng = location.lng
    postingForm.From = location.title || location.address
  } else {
    postingForm.ToLat = location.lat
    postingForm.ToLng = location.lng
    postingForm.To = location.title || location.address
  }
  
  // 如果是第一个点，将地图中心移动到此位置
  if (markers.value.length === 1) {
    mapCenter.value = { latitude: location.lat, longitude: location.lng }
  }
}

// 真实API实现示例 (替换模拟搜索功能)
async function searchLocations(type) {
    
    console.log('搜索位置:')
  const keyword = postingForm[type]
  if (!keyword) {
    suggestions[type] = []
    return
  }
  
   try {
    // 1. 添加详细的日志记录
    console.log('搜索关键词:', keyword)
    console.log('发送API请求...')
    
    // 2. 调用API
    const res = await API_TENCENT_MAP_SUGGESTION_GET(keyword)
    
    // 3. 添加响应检查
    if (!res) {
      throw new Error('API调用成功但未返回响应')
    }
    
    // 4. 详细的响应日志
    console.log('API响应:', res)
    
    // 5. 修复响应处理
    // 注意：腾讯地图API返回的结构是 { status, data }
    if (res.status === 0 && res.data) {
      suggestions[type] = res.data.map(item => ({
        title: item.title,
        address: item.address,
        lat: item.location.lat,
        lng: item.location.lng,
        type
      }))
    } else {
      // 处理API返回的错误
      throw new Error(`API错误: ${res.message || '未知错误'}`)
    }
  } catch (err) {
    // 6. 更详细的错误处理
    console.error('位置搜索失败:', {
      error: err,
      requestUrl: 'https://apis.map.qq.com/ws/place/v1/suggestion',
      params: { keyword, region: '上海' }
    })
    }
}
// 显示建议列表
function showSuggestions(type) {
  suggestionsVisible[type] = true
  activeInput.value = type
  if (postingForm[type]) {
    searchLocations(type)
  }
}

// 隐藏建议列表
function hideSuggestions(type) {
  // 延迟隐藏，让用户有时间点击建议项
  setTimeout(() => {
    suggestionsVisible[type] = false
  }, 200)
}

// 选择建议项
function selectSuggestion(item) {
  // 隐藏建议列表
  suggestionsVisible[item.type] = false
  activeInput.value = ''
  
  // 添加标记点
  addMarker({
    lat: item.lat,
    lng: item.lng,
    title: item.title,
    address: item.address
  }, item.type)
  
  // 将地图移动到标记点位置
  mapCenter.value = { latitude: item.lat, longitude: item.lng }
  zoomLevel.value = 15
}

// 处理标记点点击
function handleMarkerTap(e) {
  const marker = markers.value.find(m => m.id === e.detail.markerId)
  if (marker) {
    uni.showToast({
      title: marker.title,
      icon: 'none'
    })
  }
}

// 组件挂载时初始化地图
onMounted(() => {
  // 初始设置：空白地图（仅上海市中心）
  markers.value = []
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

.block-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: #f0f8ff;
  border-radius: 20px;
  font-size: 13px;
  color: #1989fa;
  cursor: pointer;
  transition: all 0.2s;
}

.block-actions:active {
  background: #e1f0ff;
}

.action-text {
  margin-top: 1px;
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