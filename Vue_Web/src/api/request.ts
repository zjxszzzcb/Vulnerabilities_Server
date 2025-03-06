import axios from 'axios'
import { useUserStore } from '../store/modules/user'
const service = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_API,
    timeout: 3000000,
    // 跨域时候允许携带凭证
    // withCredentials: true
})

// 在实例上设置请求拦截器
service.interceptors.request.use(
    function(config:any) {
        // 在这里可以在发送请求之前做一些事情，比如设置token
        const { token } = useUserStore()
        if (token) {
            config.headers["Authorization"] = token;
        }
        return config;
    },
    error => {
        // 请求错误处理
        return Promise.reject(error);
    }
);
export default service
