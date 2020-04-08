import axios from '../utils/axios';
import { ILoginResponse, ISignUp, IUser } from '../interfaces/auth';

export class AuthApi {
  async login(email: string, password: string): Promise<ILoginResponse> {
    const { data } = await axios.post('/auth/login', { email, password });
    return data;
  }

  async signUp(signUpData: ISignUp): Promise<IUser> {
    const { data } = await axios.post('/auth/register', signUpData);
    return data;
  }
}
