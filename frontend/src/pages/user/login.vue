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
       <nut-button block type="primary">注册账号</nut-button>
    </nut-col>
  </nut-row>
</nut-popup>


</template>

<script setup lang="ts">
import { reactive, ref, toRefs } from 'vue'

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


const showBottom = ref(false)
async function handleLogin() {
  if (!loginData.tel || !loginData.password) {
    uni.showToast({ title: '请输入手机号和密码', icon: 'none' });
    return;
  }

  try {
    const response = await uni.request({
      url: 'http://100.80.26.241:3001/login',  // 后端 Flask 服务地址
      method: 'POST',
      data: {
        Tel: loginData.tel,
        password: loginData.password
      },
      header: {
        'Content-Type': 'application/json'
      }
    });

    const { statusCode, data } = response;
    console.log('响应状态:', statusCode, '响应数据:', data);
    // if (statusCode === 200) {
    //   uni.showToast({ title: '登录成功', icon: 'success' });
    //   console.log('token:', data.token);
    //   // 你可以在这里保存 token，例如放到 localStorage、Pinia 等
    // } else {
    //   uni.showToast({ title: data.error || '登录失败', icon: 'none' });
    // }
  } catch (err) {
    console.error('请求失败:', err);
    uni.showToast({ title: '请求失败', icon: 'none' });
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