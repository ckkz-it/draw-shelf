import { action, computed, observable } from 'mobx';
import jwt from 'jsonwebtoken';

import { jwtSecret } from '../config';
import { AuthApi } from '../apis/auth-api';
import { IJWTPayload, ISignUp } from '../interfaces/auth';
import { UserStore } from './user-store';
import { storageService } from '../services/storage-service';

export class AuthStore {
  private accessTokenKey = 'access';
  private refreshTokenKey = 'refresh';

  @observable public accessToken: string | null = null;
  @observable public refreshToken: string | null = null;

  @observable public isLoading = false;
  @observable public loginError: any = null;

  constructor(private api: AuthApi, private userStore: UserStore) {
    this.setAccessToken(storageService.getItem(this.accessTokenKey));
    this.setRefreshToken(storageService.getItem(this.refreshTokenKey));
    if (this.accessToken) {
      jwt.verify(this.accessToken, jwtSecret, { algorithms: ['HS256'] }, (err, decoded) => {
        if (!err) {
          this.userStore.setUser((decoded as IJWTPayload).user);
        }
      });
    }
  }

  @computed get isAuthenticated() {
    return this.userStore.user !== null;
  }

  @action setAccessToken(token: string | null) {
    if (token) {
      storageService.setItem(this.accessTokenKey, token);
      this.accessToken = token;
    } else {
      storageService.removeItem(this.accessTokenKey);
      this.accessToken = null;
    }
  }

  @action setRefreshToken(token: string | null) {
    if (token) {
      storageService.setItem(this.refreshTokenKey, token);
      this.refreshToken = token;
    } else {
      storageService.removeItem(this.refreshTokenKey);
      this.refreshToken = null;
    }
  }

  @action async login(email: string, password: string) {
    const data = await this.api.login(email, password);
    this.setAccessToken(data.access);
    this.setRefreshToken(data.refresh);
    this.userStore.setUser((jwt.decode(data.access) as IJWTPayload).user);
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
