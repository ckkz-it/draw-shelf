import { action, computed, observable } from 'mobx';
import jwt from 'jsonwebtoken';

import { jwtSecret, storagePrefix } from '../config';
import { AuthApi } from '../apis/auth-api';
import { ISignUp, IUser } from '../interfaces/auth';
import { UserStore } from './user-store';

export class AuthStore {
  private accessTokenKey = storagePrefix + 'access';
  private refreshTokenKey = storagePrefix + 'refresh';

  @observable public accessToken: string | null = null;
  @observable public refreshToken: string | null = null;

  @observable public isLoading = false;
  @observable public loginError: any = null;

  constructor(private api: AuthApi, private userStore: UserStore) {
    this.setAccessToken(window.localStorage.getItem(this.accessTokenKey));
    this.setRefreshToken(window.localStorage.getItem(this.refreshTokenKey));
    if (this.accessToken) {
      jwt.verify(this.accessToken, jwtSecret, { algorithms: ['HS256'] }, (err, decoded) => {
        if (!err) {
          this.userStore.setUser(decoded as IUser);
        }
      });
    }
  }

  @computed get isAuthenticated() {
    return this.userStore.user !== null;
  }

  @action setAccessToken(token: string | null) {
    if (token) {
      window.localStorage.setItem(this.accessTokenKey, token);
      this.accessToken = token;
    } else {
      window.localStorage.removeItem(this.accessTokenKey);
      this.accessToken = null;
    }
  }

  @action setRefreshToken(token: string | null) {
    if (token) {
      window.localStorage.setItem(this.refreshTokenKey, token);
      this.refreshToken = token;
    } else {
      window.localStorage.removeItem(this.refreshTokenKey);
      this.refreshToken = null;
    }
  }

  @action async login(email: string, password: string) {
    const data = await this.api.login(email, password);
    this.setAccessToken(data.access);
    this.setRefreshToken(data.refresh);
    this.userStore.setUser(jwt.decode(data.access) as IUser);
  }

  @action async signUp(signUpData: ISignUp) {
    await this.api.signUp(signUpData);
  }

  @action logout() {
    this.setAccessToken(null);
    this.setRefreshToken(null);
    this.userStore.setUser(null);
  }
}
