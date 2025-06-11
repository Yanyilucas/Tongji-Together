<template>
  <view class="trip-card-container">
    <view class="map-preview" v-if="showMap">
      <map
        :latitude="centerPoint.lat"
        :longitude="centerPoint.lng"
        :scale="mapZoom"
        :markers="markers"
        :polyline="polyline"
        enable-3D="false"
        enable-zoom="false"
        enable-scroll="false"
        enable-rotate="false"
        class="map-instance"
      />
      <view class="map-overlay"></view>
    </view>

    <view class="trip-info">
      <view class="route-line">
        <view class="route-point">
          <view class="point-indicator start"></view>
          <view class="point-label">{{ item.From }}</view>
        </view>
        <view class="route-divider">
          <view class="divider-line"></view>
        </view>
        <view class="route-point">
          <view class="point-indicator end"></view>
          <view class="point-label">{{ item.To }}</view>
        </view>
      </view>

      <view class="trip-meta">
        <view class="meta-row">
          <text class="meta-label">出发时间:</text>
          <text>{{ formatTime(item.DepartureTime) }}</text>
        </view>
         <view class="meta-row">
          <text class="meta-label">联系人:</text>
          <text>{{ item.Name}}</text>
        </view>
        <view class="meta-row">
          <text class="meta-label">联系电话:</text>
          <text>{{ item.Tel }}</text>
        </view>
        <view class="meta-grid">
          <view class="meta-badge">
            <text>{{ item.PlateNumber }}</text>
          </view>
          <view class="meta-badge">
            <text>{{ item.JoinCount }}/{{ item.SeatsAvailable }}座</text>
          </view>
          <view class="meta-badge price">
            <text>¥{{ item.Fare }}</text>
          </view>
        </view>
         <nut-button 
          v-if="showMap"
          size="small"
          type="info"
          block
          @click = "joinTrip">
            <template #icon>
                <nut-icon name="plus" size="16"></nut-icon>
            </template>
            拼车
          </nut-button>

          <nut-button 
          v-else
          size="small"
          type="info"
          block
          plain
          @click = "cancelTrip">
            <template #icon>
                <nut-icon name="minus" size="16"></nut-icon>
            </template>
            取消
          </nut-button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  showMap: {
    type: Boolean,
    default: true
  }
})

// 格式化时间显示
function formatTime(time) {
  const date = new Date(time)
  return `${date.getMonth()+1}/${date.getDate()} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 计算中心点
const centerPoint = computed(() => ({
  lat: (props.item.FromLat + props.item.ToLat) / 2,
  lng: (props.item.FromLng + props.item.ToLng) / 2
}))

// 标记点 - 不使用静态图标
const markers = computed(() => [
  {
    id: 1,
    latitude: props.item.FromLat,
    longitude: props.item.FromLng,
    width: 18,
    height: 18,
    color: '#1989fa',
    customCallout: {
      display: 'BYCLICK',
      anchorY: 0
    }
  },
  {
    id: 2,
    latitude: props.item.ToLat,
    longitude: props.item.ToLng,
    width: 18,
    height: 18,
    color: '#ee0a24',
    customCallout: {
      display: 'BYCLICK',
      anchorY: 0
    }
  }
])

// 路线
const polyline = computed(() => [
  {
    points: [
      { latitude: props.item.FromLat, longitude: props.item.FromLng },
      { latitude: props.item.ToLat, longitude: props.item.ToLng }
    ],
    color: '#3c9cff',
    width: 4,
    arrowLine: true
  }
])

// 动态计算缩放级别
const mapZoom = computed(() => {
  const latDiff = Math.abs(props.item.FromLat - props.item.ToLat)
  const lngDiff = Math.abs(props.item.FromLng - props.item.ToLng)
  const maxDiff = Math.max(latDiff, lngDiff)
  
  if (maxDiff < 0.01) return 16
  if (maxDiff < 0.05) return 14
  if (maxDiff < 0.1) return 12
  return 10
})


function joinTrip() {
  // 这里可以添加拼车逻辑
  console.log('加入拼车:', props.item)
  uni.showToast({
    title: '已加入拼车',
    icon: 'success'
  })
}

function cancelTrip() {
  // 这里可以添加取消拼车逻辑
  console.log('取消拼车:', props.item)
  uni.showToast({
    title: '已取消拼车',
    icon: 'success'
  })
}

</script>

<style scoped>
/* 整体卡片容器 */
.trip-card-container {
  margin: 16px 12px;
  border-radius: 16px;
  overflow: hidden;
  background: #fff;
  box-shadow: 
    0 6px 16px rgba(0, 0, 0, 0.08),
    0 3px 6px rgba(0, 0, 0, 0.04);
  position: relative;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.trip-card-container:active {
  transform: translateY(2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

/* 地图预览区域 */
.map-preview {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: linear-gradient(160deg, #e3eeff, #f0f7ff);
}

/* 地图实例 - 关键样式修正 */
.map-instance {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 120%;  /* 增加高度以填充容器 */
}

/* 地图顶部渐变遮罩 */
.map-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 40px;
  background: linear-gradient(to bottom, rgba(0,0,0,0.15), transparent);
  z-index: 10;
}

/* 行程信息区域 */
.trip-info {
  padding: 16px;
  position: relative;
  z-index: 20;
  background: #fff;
}

/* 路线显示 */
.route-line {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 14px;
}

.route-point {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.point-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
}

.point-indicator.start {
  background: #1989fa;
  box-shadow: 0 0 0 3px rgba(25, 137, 250, 0.2);
}

.point-indicator.end {
  background: #ee0a24;
  box-shadow: 0 0 0 3px rgba(238, 10, 36, 0.2);
}

.point-label {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  line-height: 1.4;
}

.route-divider {
  position: relative;
  height: 20px;
  padding-left: 5px;
}

.divider-line {
  position: absolute;
  left: 5px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: repeating-linear-gradient(
    to bottom,
    #c8d9ff,
    #c8d9ff 4px,
    transparent 4px,
    transparent 8px
  );
  margin: 0 0 0 5px;
}

/* 元信息区域 */
.trip-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.meta-row {
  display: flex;
  gap: 8px;
  font-size: 13px;
  color: #666;
}

.meta-label {
  font-weight: 500;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.meta-badge {
  background: #f5f7fa;
  border-radius: 16px;
  padding: 5px 10px;
  font-size: 12px;
  text-align: center;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meta-badge.price {
  background: rgba(60, 156, 255, 0.12);
  color: #3c9cff;
  font-weight: 600;
}
</style>