<template>
  <view class="trip-form-container">
    <!-- 地图组件 -->
    <TripMap 
      :from-address="postingForm.From" 
      :to-address="postingForm.To"
      @location-change="handleLocationChange"
    />
    
    <!-- 表单 -->
    <nut-form class="form-card">
      <nut-form-item label="出发地" required>
        <nut-input 
          v-model="postingForm.From" 
          placeholder="请输入出发地" 
          clearable
        />
      </nut-form-item>
      <nut-form-item label="目的地" required>
        <nut-input 
          v-model="postingForm.To" 
          placeholder="请输入目的地" 
          clearable
        />
      </nut-form-item>
      <nut-form-item label="出发时间" required>
        <picker 
          mode="date" 
          :value="departureDate" 
          @change="handleDateChange"
        >
          <view class="picker">
            {{ departureDateDisplay || '选择日期' }}
          </view>
        </picker>
        <picker 
          mode="time" 
          :value="departureTime" 
          @change="handleTimeChange"
        >
          <view class="picker">
            {{ departureTime || '选择时间' }}
          </view>
        </picker>
      </nut-form-item>
      <nut-form-item label="车牌号" required>
        <nut-input 
          v-model="postingForm.PlateNumber" 
          placeholder="请输入车牌号" 
          clearable
        />
      </nut-form-item>
      <nut-form-item label="可用座位数" required>
        <nut-input 
          v-model.number="postingForm.SeatsAvailable" 
          type="number" 
          placeholder="请输入可用座位数" 
        />
      </nut-form-item>
      <nut-form-item label="费用" required>
        <nut-input 
          v-model.number="postingForm.Fare" 
          type="number" 
          placeholder="请输入费用"
          prefix="¥"
        />
      </nut-form-item>
      <nut-form-item label="附加说明">
        <nut-textarea 
          v-model="postingForm.Note" 
          placeholder="请输入附加说明"
          rows="2"
        />
      </nut-form-item>
      
      <view class="submit-btn-container">
        <nut-button 
          type="primary" 
          block
          @click="submitForm"
        >
          发布行程
        </nut-button>
      </view>
    </nut-form>
  </view>
</template>

<script setup >
import { reactive, ref } from 'vue'
import TripMap from './TripMap.vue'

const postingForm = reactive({
  From: '',
  To: '',
  FromLat: 0,   // 出发地纬度
  FromLng: 0,   // 出发地经度
  ToLat: 0,     // 目的地纬度
  ToLng: 0,     // 目的地经度
  DepartureTime: '',
  SeatsAvailable: 3,
  Fare: 50,
  Note: '',
  PlateNumber: '',
})

// 日期和时间选择器相关
const departureDate = ref('')
const departureTime = ref('')
const departureDateDisplay = ref('')

// 处理位置变化事件
function handleLocationChange(data: any) {
  if (data.type === 'from') {
    postingForm.FromLat = data.latitude
    postingForm.FromLng = data.longitude
  } else if (data.type === 'to') {
    postingForm.ToLat = data.latitude
    postingForm.ToLng = data.longitude
  }
}

// 处理日期选择
function handleDateChange(e: any) {
  departureDate.value = e.detail.value
  updateDepartureTime()
}

// 处理时间选择
function handleTimeChange(e: any) {
  departureTime.value = e.detail.value
  updateDepartureTime()
}

// 更新出发时间
function updateDepartureTime() {
  if (departureDate.value && departureTime.value) {
    postingForm.DepartureTime = `${departureDate.value} ${departureTime.value}`
    
    // 格式化日期显示
    const dateObj = new Date(`${departureDate.value}T${departureTime.value}:00`)
    departureDateDisplay.value = dateObj.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'short'
    })
  }
}

// 表单提交
function submitForm() {
  // 验证表单
  if (!postingForm.From || !postingForm.To) {
    uni.showToast({ title: '请填写出发地和目的地', icon: 'none' })
    return
  }
  
  if (!postingForm.DepartureTime) {
    uni.showToast({ title: '请选择出发时间', icon: 'none' })
    return
  }
  
  if (!postingForm.PlateNumber) {
    uni.showToast({ title: '请填写车牌号', icon: 'none' })
    return
  }
  
  // 表单验证通过，提交逻辑...
  console.log('表单提交:', postingForm)
  uni.showToast({ title: '行程发布成功！' })
  
  // 重置表单
  setTimeout(() => {
    postingForm.From = ''
    postingForm.To = ''
    postingForm.DepartureTime = ''
    postingForm.PlateNumber = ''
    postingForm.SeatsAvailable = 3
    postingForm.Fare = 50
    postingForm.Note = ''
    departureDate.value = ''
    departureTime.value = ''
    departureDateDisplay.value = ''
  }, 1500)
}
</script>

<style scoped>
.trip-form-container {
  padding: 16px;
  padding-bottom: 40px;
}

.form-card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-top: 20px;
}

.picker {
  padding: 12px 16px;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  margin-top: 8px;
  font-size: 14px;
  color: #333;
}

.submit-btn-container {
  margin-top: 24px;
}
</style>