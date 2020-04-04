import { action, observable } from 'mobx';
import jwt from 'jsonwebtoken';

import { storagePrefix } from '../config';
import { AuthApi } from '../apis/auth-api';
import { ISignUp, IUser } from '../interfaces/auth';

export class AuthStore {
  private accessTokenKey = storagePrefix + 'access';
  private refreshTokenKey = storagePrefix + 'refresh';
  private api: AuthApi;

  @observable public accessToken: string | null = null;
  @observable public refreshToken: string | null = null;
  @observable public user: IUser | null = null;

  constructor(authApi: AuthApi) {
    this.api = authApi;
    this.setAccessToken(window.localStorage.getItem(this.accessTokenKey));
    this.setRefreshToken(window.localStorage.getItem(this.refreshTokenKey));
  }

  @action
  setAccessToken(token: string | null) {
    if (token) {
      window.localStorage.setItem(this.accessTokenKey, token);
      this.accessToken = token;
    } else {
      window.localStorage.removeItem(this.accessTokenKey);
      this.accessToken = null;
    }
  }

  @action
  setRefreshToken(token: string | null) {
    if (token) {
      window.localStorage.setItem(this.refreshTokenKey, token);
      this.refreshToken = token;
    } else {
      window.localStorage.removeItem(this.refreshTokenKey);
      this.refreshToken = null;
    }
  }

  @action
  setUser(user: IUser) {
    this.user = user;
  }

  @action
  async login(email: string, password: string) {
    const data = await this.api.login(email, password);
    this.setAccessToken(data.access);
    this.setRefreshToken(data.refresh);
    this.setUser(jwt.decode(data.access) as IUser);
  }

  @action
  async signUp(signUpData: ISignUp) {
    await this.api.signUp(signUpData);
  }
}
