


import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api' // Backend runs on port 5000

export const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  } catch (error) {
    console.error('Failed to upload file:', error)
    throw error
  }
}


