import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// API方法
export const financeAPI = {
  // 获取所有交易记录
  getTransactions() {
    return api.get('/transactions')
  },
  
  // 添加交易记录
  addTransaction(data) {
    return api.post('/transactions', data)
  },
  
  // 删除交易记录
  deleteTransaction(id) {
    return api.delete(`/transactions/${id}`)
  },
  
  // 获取统计信息
  getStatistics() {
    return api.get('/statistics')
  },
  
  // 搜索交易记录
  searchTransactions(keyword) {
    return api.get('/search', { params: { keyword } })
  }
}

export default api