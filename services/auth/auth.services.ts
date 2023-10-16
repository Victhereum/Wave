import axiosClient from "../../helpers/apiClient";

interface IAuthLogin {
    phone_no: string;
    otp: string;
}
interface IAuthRegister {
    phone_no: string;
    name: string;
}

class Auth {
    async login({ phone_no, otp }: IAuthLogin) {
        return await axiosClient.post('/ausers/phone/otp/', {
            phone_no,
            otp
        })
    }

    async register({ phone_no, name }: IAuthRegister) {
        return await axiosClient.post('/users/register/', {
            phone_no,
            name
        })
    }

    async sendOtp({ phone_no }: { phone_no: string }) {
        return await axiosClient.get(`/users/phone/otp?phone_no=${phone_no}`)
    }



}

const authService = new Auth()

export default authService