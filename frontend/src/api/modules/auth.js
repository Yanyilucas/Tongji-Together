import { request } from '../request'

export default {
  // 登录请求
  API_LOGIN_POST(data = {}) {
    return request({
      url: '/login',
      method: 'post',
      data
    })
  },

  // 注册请求
  API_REGISTER_POST(data = {}) {
    return request({
      url: '/register',
      method: 'post',
      data
    })
  },

  // 获取用户信息
  API_USERINFO_GET() {
    return request({
      url: '/userinfo',
      method: 'get',
    })
  },

  // 注册车主
  API_REGISTER_DRIVER_POST() {
    return request({
      url: '/register_driver',
      method: 'post',
    })
  },

  // 注销车主
  API_UNREGISTER_DRIVER_POST() {
    return request({
      url: '/unregister_driver',
      method: 'post',
    })
  },

  // 腾讯地图 搜索建议
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

  // 腾讯地图 路径规划
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

    // 车主发布行程
    API_DRIVERPOSTING_POST(data = {}) {
    return request({
      url: '/driverposting',
      method: 'post',
      data
    })
  },
  
}