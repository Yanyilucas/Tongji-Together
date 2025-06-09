import { defineStore } from 'pinia'
import { piniaStore } from '.'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',
    userInfo: null
  }),
  actions: {
    setToken(token) {
      this.token = token
    },
    clearToken() {
      this.token = ''
    },
    setUserInfo(info) {
      this.userInfo = info
    },
    clearUserInfo() {
      this.userInfo = null
    },
    logout() {
      this.clearToken()
      this.clearUserInfo()
    }
  },
  persist: true // 开启持久化，写入 localStorage 或 uniStorage
})

// 用于非 setup 语法下调用
export function useOutsideUserStore() {
  return useUserStore(piniaStore)
}