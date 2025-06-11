<template>
  <view class="trip-form-container">
    <!-- 地图容器区块 -->
    <view class="map-block">
      <!-- 区块标题 -->
      <view class="block-header">
        <text class="block-title">行程检索</text>
      </view>
      
      <!-- 位置输入区域 -->
      <view class="location-inputs">
        <view class="input-row">
          <nut-icon name="location" size="16" ></nut-icon>
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
          <nut-icon name="location" size="16"></nut-icon>
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
            <nut-icon name="location" size="14"></nut-icon>
          </view>
          <view class="suggestion-content">
            <text class="suggestion-title">{{ item.title }}</text>
            <text class="suggestion-address">{{ item.address }}</text>
          </view>
        </view>
      </view>

      <view class="searchbar-controls">
        <nut-button type="info" size="small" plain @click="searchBarFilter">
            <template #icon>
              <nut-icon name="search" size="16"></nut-icon>
            </template>
        </nut-button>
        <nut-button type="default" size="small" plain @click="searchBarClear">
            <template #icon>
              <nut-icon name="del" size="16"></nut-icon>
            </template>
        </nut-button>
      </view>
      
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, computed} from 'vue'

// 表单数据 postingFormAddrset 初始化为响应式对象
const postingFormAddrset = reactive({
  From: '',
  To: '',
  FromLat: 0,
  FromLng: 0,
  ToLat: 0,
  ToLng: 0
})

const {API_TENCENT_MAP_SUGGESTION_GET} = useRequest()

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

// 清空搜索栏
function searchBarClear() {
  postingFormAddrset.From = ''
  postingFormAddrset.To = ''
  postingFormAddrset.FromLat = 0
  postingFormAddrset.FromLng = 0
  postingFormAddrset.ToLat = 0
  postingFormAddrset.ToLng = 0
}

function searchBarFilter() {
  // 这里可以添加搜索过滤逻辑
  // 例如，调用API获取符合条件的行程数据
  console.log('搜索过滤功能待实现')
}


// 添加标记点
function addMarker(location, label) {
  // 设置对应的标记，仅保存经纬度
  if (label === 'From') {
    postingFormAddrset.FromLat = location.lat
    postingFormAddrset.FromLng = location.lng
    postingFormAddrset.From = location.title || location.address
  } else {
    postingFormAddrset.ToLat = location.lat
    postingFormAddrset.ToLng = location.lng
    postingFormAddrset.To = location.title || location.address
  }
}



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



</script>

<style scoped>
.trip-form-container {
  padding: 16px;
}

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


/* 搜索栏控制按钮 */
.searchbar-controls {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.9);
  border-top: 1px solid #f5f5f5;
}

/* 响应式调整 */
@media (min-width: 768px) {
  .map-block {
    margin-bottom: 32px;
  }
}

/* 小程序适配 */
/* #ifdef MP-WEIXIN */
/* #endif */
</style>