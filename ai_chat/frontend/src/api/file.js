import request from './request'

export const fileApi = {
  // 上传文件
  uploadFile(file, onProgress = null) {
    const formData = new FormData()
    formData.append('file', file)
    
    return request.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: onProgress
    })
  },

  // 获取文件列表
  getFiles() {
    return request.get('/files')
  },

  // 下载文件
  downloadFile(filename) {
    return request.get(`/files/${filename}`, {
      responseType: 'blob'
    })
  }
}