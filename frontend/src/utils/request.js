import axios from 'axios'

// 创建axios实例
const service = axios.create({
  baseURL: '/api',
  timeout: 8000 ,   // 请求超时时间8秒
  withCredentials: true, 
})


service.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)
// 响应拦截器：后端返回数据统一处理
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // 统一错误提示
    if (error.response) {
      console.error('请求错误：', error.response.data)
    } else {
      console.error('网络连接失败')
    }
    return Promise.reject(error)
  }
)

export default service