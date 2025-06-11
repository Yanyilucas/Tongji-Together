<template>
  <view class="trip-form-container">
    <!-- 地图组件 -->
    <TripMap 
    v-model:modelValue="postingForm"
    />
    <!-- 表单 : 出发地和目的地的搜索应交给地图模块-->
    <nut-form class="form-card">
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

<script setup>
import { ref, reactive } from 'vue'
import TripMap from './TripMap.vue'
const  { API_DRIVERPOSTING_POST} = useRequest()
// 表单数据
const postingForm = reactive({
  From: '', 
  To: '',
  FromLat: 0,
  FromLng: 0,
  ToLat: 0,
  ToLng: 0,
  DepartureTime: '',
  SeatsAvailable: 1,
  Fare: 50,
  Note: '',
  PlateNumber: '',
})

// 日期和时间选择器相关
const departureDate = ref('')
const departureTime = ref('')
const departureDateDisplay = ref('')


// 处理日期选择
function handleDateChange(e) {
  departureDate.value = e.detail.value
  updateDepartureTime()
}

// 处理时间选择
function handleTimeChange(e) {
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
  for (const key in postingForm) {
  console.log(`${key}:`, postingForm[key])
}
  try {
    // 调用API提交数据
    API_DRIVERPOSTING_POST(postingForm)
    uni.showToast({ title: '行程发布成功', icon: 'success' })
  } catch (error) {
    console.error('提交异常:', error)
    uni.showToast({ title: error.error, icon: 'none' })
  }

  
  // // 重置表单
  // setTimeout(() => {
  //   postingForm.From = ''
  //   postingForm.To = ''
  //   postingForm.DepartureTime = ''
  //   postingForm.PlateNumber = ''
  //   postingForm.SeatsAvailable = 1
  //   postingForm.Fare = 50
  //   postingForm.Note = ''
  //   departureDate.value = ''
  //   departureTime.value = ''
  //   departureDateDisplay.value = ''
  // }, 1500)
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