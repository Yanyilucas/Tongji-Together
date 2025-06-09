<template>

  <view class="avatar-wrapper">
    <nut-avatar size="large" shape="round" bg-color="#FA2C19" custom-color="#ffffff">
      <nut-icon name="my" size="50"></nut-icon>
    </nut-avatar>
  </view>

  <nut-form>
    <nut-form-item label="手机号">
      <nut-input
        v-model="loginData.tel"
        class="nut-input-text"
        placeholder="请输入手机号"
        type="text"
      />
    </nut-form-item>
    <nut-form-item label="密码">
      <nut-input
        v-model="loginData.password"
        class="nut-input-text"
        placeholder="请输入密码"
        type="password"
        :password="true"
      />
    </nut-form-item>
  </nut-form>
  <nut-row>
    <nut-col :span="12">
       <nut-button block type="primary" @click="handleLogin">登录</nut-button>
    </nut-col>
    <nut-col :span="12">
      <nut-button block type="primary" plain @click="showBottom = true"> 注册 </nut-button>
    </nut-col>
  </nut-row>


<!-- 这段是注册界面的弹出框 -->
  <nut-popup position="bottom" round :custom-style="{ height: '80%' }" v-model:visible="showBottom">

  <nut-form>
    <nut-divider :custom-style="{ color: '#1989fa', borderColor: '#1989fa', padding: '0 16px' }">
      注册账号
    </nut-divider>
    <nut-form-item label="用户名">
      <nut-input
        v-model="registerData.name"
        class="nut-input-text"
        placeholder="请输入用户名"
        type="text"
      />
    </nut-form-item>
    <nut-form-item label="手机号">
      <nut-input
        v-model="registerData.tel"
        class="nut-input-text"
        placeholder="请输入手机号"
        type="text"
      />
    </nut-form-item>
    <nut-form-item label="密码">
      <nut-input
        v-model="registerData.password"
        class="nut-input-text"
        placeholder="请输入密码"
        type="password"
        :password="true"
      />
    </nut-form-item>
    <nut-form-item label="确认密码">
      <nut-input
        v-model="registerData.confirmPassword"
        class="nut-input-text"
        placeholder="请再次输入密码"
        type="password"
        :password="true"
      />
    </nut-form-item>
  </nut-form>

  <nut-cell>
    <nut-radio-group
    v-model="registerData.isDriver"
    direction="horizontal"
    style="display: flex; justify-content: center"
    >
    <nut-radio :label="true" size="large">我是司机</nut-radio>
    <nut-radio :label="false" size="large">我是乘客</nut-radio>
  </nut-radio-group>
  </nut-cell>
  <nut-row>
    <nut-col :span="24">
       <nut-button block type="primary" @click="handleRegister">注册账号</nut-button>
    </nut-col>
  </nut-row>
</nut-popup>


</template>

<script setup>
import { reactive, ref} from 'vue'
import { useRequest } from '@/api'
const {API_LOGIN_POST,API_REGISTER_POST} = useRequest()



// 表单数据响应式变量
const showBottom = ref(false)
const loginData = reactive({
  tel: '',
  password: ''
})
const registerData = reactive({
  name: '',
  tel: '',
  password: '',
  confirmPassword: '',
  isDriver: false
})


// 处理登录逻辑
async function handleLogin() {
  if (!loginData.tel || !loginData.password) {
    uni.showToast({ title: '请输入手机号和密码', icon: 'none' })
    return
  }
  try {
    const res = await API_LOGIN_POST({
      Tel: loginData.tel,
      password: loginData.password
    })
    uni.setStorageSync('token', res.token)  // 存储 token
    uni.navigateBack()
    uni.showToast({ title: res.message || '登录成功', icon: 'success' })

  } catch (err) {
  console.error('登录失败:', err)

  const message =
    err?.response?.data?.error ||        // 后端自定义返回
    err?.message ||                      // Axios 错误消息
    '登录失败'                           // 兜底
  uni.showToast({ title: message, icon: 'none' })
}
}
//  处理注册逻辑
async function handleRegister() {
  const { name, tel, password, confirmPassword, isDriver } = registerData

  // 基础校验
  if (!name || !tel || !password || !confirmPassword) {
    uni.showToast({ title: '请完整填写注册信息', icon: 'none' })
    return
  }
  if (password !== confirmPassword) {
    uni.showToast({ title: '两次密码不一致', icon: 'none' })
    return
  }

  try {
    const res = await API_REGISTER_POST({
      name,
      tel,
      password,
      confirmPassword,
      isDriver
    })
    uni.showToast({ title: res.message || '注册成功', icon: 'success' })
    // 保存 token，可选
    loginData.tel = tel
    console.log('注册获得 token:', res.token)
    showBottom.value = false          // 关闭弹窗
    loginData.tel = tel               // 回填登录表单方便直接登录
  } catch (err) {
    const msg =
      err?.response?.data?.error ||
      err?.message ||
      '注册失败'
    uni.showToast({ title: msg, icon: 'none' })
  }
}
</script>

<style scoped>
.avatar-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20rpx 0;
}
</style>