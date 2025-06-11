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
  },

  // 
  API_TENCENT_MAP_SUGGESTION_GET(keyword){
    return request({
      url: 'https://apis.map.qq.com/ws/place/v1/suggestion',
      method: 'get',
      params:{
        keyword,
        region: '上海',
        key: import.meta.env.VITE_TENCENT_MAP_API_KEY, // 腾讯地图API密钥
      }
    })
  },

  API_TENCENT_MAP_ROUTE_GET(from, to) {
    return request({
      url: 'https://apis.map.qq.com/ws/direction/v1/driving',
      method: 'get',
      params: {
        from,
        to,
        region: '上海',
        key: import.meta.env.VITE_TENCENT_MAP_API_KEY, // 腾讯地图API密钥
      }
    })
  },


}