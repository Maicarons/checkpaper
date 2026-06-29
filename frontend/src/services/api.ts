import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      // 服务器返回错误
      const { status, data } = error.response
      if (status === 401) {
        // 未授权，可以跳转到登录页
        console.error('未授权访问')
      } else if (status === 413) {
        console.error('文件太大')
      }
      return Promise.reject(error)
    } else if (error.request) {
      // 请求发送失败
      console.error('网络错误，请检查网络连接')
      return Promise.reject(error)
    } else {
      console.error('请求配置错误')
      return Promise.reject(error)
    }
  }
)

// 文档API
export const documentApi = {
  // 上传文档
  upload: (formData: FormData) => {
    return api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // 获取文档列表
  list: (params?: { page?: number; page_size?: number; status?: string }) => {
    return api.get('/documents/', { params })
  },

  // 获取文档详情
  get: (id: string) => {
    return api.get(`/documents/${id}`)
  },

  // 删除文档
  delete: (id: string) => {
    return api.delete(`/documents/${id}`)
  },

  // 解析文档
  parse: (id: string) => {
    return api.post(`/documents/${id}/parse`)
  },

  // 下载文档
  download: (id: string) => {
    return api.get(`/documents/${id}/download`, {
      responseType: 'blob',
    })
  },
}

// 验证API
export const validationApi = {
  // 开始验证
  startValidation: (data: {
    document_id: string
    validation_types?: string[]
    options?: Record<string, any>
  }) => {
    return api.post('/validation/start', data)
  },

  // 快速验证
  quickValidation: (documentId: string, validationTypes?: string[]) => {
    return api.post('/validation/quick', null, {
      params: {
        document_id: documentId,
        validation_types: validationTypes,
      },
    })
  },

  // 获取任务列表
  listTasks: (params?: {
    page?: number
    page_size?: number
    document_id?: string
    status?: string
  }) => {
    return api.get('/validation/tasks', { params })
  },

  // 获取任务详情
  getTask: (taskId: string) => {
    return api.get(`/validation/tasks/${taskId}`)
  },

  // 获取验证结果
  getResults: (taskId: string) => {
    return api.get(`/validation/tasks/${taskId}/results`)
  },

  // 取消任务
  cancelTask: (taskId: string) => {
    return api.post(`/validation/tasks/${taskId}/cancel`)
  },

  // 获取验证类型
  getTypes: () => {
    return api.get('/validation/types')
  },
}

// 报告API
export const reportApi = {
  // 获取报告列表
  list: (params?: { page?: number; page_size?: number; document_id?: string }) => {
    return api.get('/reports/', { params })
  },

  // 获取报告详情
  get: (id: string) => {
    return api.get(`/reports/${id}`)
  },

  // 下载报告
  downloadReport: (id: string, format: string = 'md') => {
    return api.get(`/reports/${id}/download`, {
      params: { format },
      responseType: 'blob',
    })
  },

  // 删除报告
  delete: (id: string) => {
    return api.delete(`/reports/${id}`)
  },
}

export default api
