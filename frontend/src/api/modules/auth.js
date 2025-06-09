import { request } from '../request'

export default {
  API_LOGIN_POST(data = {}) {
    return request({
      url: '/login',
      method: 'post',
      data
    })
  },

  // ... 原有 API_DEMO_GET, API_DEMO_POST 可保留
}