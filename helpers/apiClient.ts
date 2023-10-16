import axios from 'axios'
import globalBaseUrl from './globalBaseUrl'

const axiosClient = axios.create({
    baseURL: globalBaseUrl,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
    }
})

axiosClient.interceptors.request.use(
    async (config) => {
        const token = ''
       
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
            console.log(`Bearer ${token}`)
        }

        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default axiosClient
