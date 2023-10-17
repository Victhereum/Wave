import axios from 'axios'
import globalBaseUrl from './globalBaseUrl'
import { getToken } from '../states/asyncStore/token'

const videoApiClient = axios.create({
    baseURL: globalBaseUrl,
    headers: {
        Accept: 'application/json',
        'Content-Type': ' multipart/form-data'
    }
})

videoApiClient.interceptors.request.use(
    async (config) => {
        const token = await getToken()
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }

        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default videoApiClient
