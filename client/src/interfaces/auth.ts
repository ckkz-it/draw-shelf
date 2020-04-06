export type ISignUp = {
  name: string;
  email: string;
  phone: string;
  password: string;
};

export type ILoginResponse = {
  access: string;
  refresh: string;
};

export interface IUser {
  id: string;
  name: string;
  email: string;
  phone: string;
  createdAt: Date;
}

export type IJWTPayload = {
  user: IUser;
  exp: number;
  iat: number;
};
