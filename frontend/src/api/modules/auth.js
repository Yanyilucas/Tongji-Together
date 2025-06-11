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
      url: '/post_driver_posting',
      method: 'post',
      data:{
        From: data.From, // 出发地
        To: data.To, // 目的地
        FromLat: data.FromLat, // 出发地纬度
        FromLng: data.FromLng, // 出发地经度
        ToLat: data.ToLat, // 目的地纬度
        ToLng: data.ToLng, // 目的地经度
        DepartureTime: data.DepartureTime, // 出发时间
        SeatsAvailable: data.SeatsAvailable, // 可用座位数
        Fare: data.Fare, // 费用
        PlateNumber: data.PlateNumber, // 车牌号
        Note: data.Note, // 备注
      }
    })
  },


  // 获取车主发布的行程
  API_DRIVERPOSTING_GET(From,To,FromLat, FromLng, ToLat, ToLng) {
    return request({
      url: '/get_driver_postings',
      method: 'get',
      params: {
        From, // 出发地
        To, // 目的地
        FromLat, // 出发地纬度
        FromLng, // 出发地经度
        ToLat, // 目的地纬度
        ToLng, // 目的地经度
      }
    })
  },


  API_MYTRIP_GET(){
    return request({
      url: '/my_trip',
      method: 'get',
    })
  },
  
  API_JOINTRIP_POST(data = {}) {
    return request({
      url: '/join_trip',
      method: 'post',
      data: {
        PostingId: data.PostingId, // 行程ID
        UserId: data.UserId, // 用户ID
      }
    })
  },

  API_CANCELTRIP_POST(data = {}) {
    return request({
      url: '/cancel_trip',
      method: 'post',
      data: {
        PostingId: data.PostingId, // 行程ID
        UserId: data.UserId, // 用户ID
      }
    })
  }

}