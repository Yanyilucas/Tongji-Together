import { request } from '../request'

export default {
  API_LOGIN_POST(data = {}) {
    return request({
      url: '/login',
      method: 'post',
      data
    })
  },

  API_REGISTER_POST(data = {}) {
    return request({
      url: '/register',
      method: 'post',
      data
    })
  },

  API_USERINFO_GET() {
    return request({
      url: '/userinfo',
      method: 'get',
    })
  },

  API_REGISTER_DRIVER_POST() {
    return request({
      url: '/register_driver',
      method: 'post',
    })
  },

  API_UNREGISTER_DRIVER_POST() {
    return request({
      url: '/unregister_driver',
      method: 'post',
    })
  }
}