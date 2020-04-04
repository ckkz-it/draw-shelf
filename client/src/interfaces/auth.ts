export interface ISignUp {
  name: string;
  email: string;
  phone: string;
  password: string;
}

export interface ILoginResponse {
  access: string;
  refresh: string;
}

export interface IUser {
  id: string;
  name: string;
  email: string;
  phone: string;
  createdAt: Date;
}
