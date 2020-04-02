import { action, observable } from 'mobx';

import { storagePrefix } from '../config';

export class AuthStore {
  private accessTokenKey = storagePrefix + 'access';
  private refreshTokenKey = storagePrefix + 'refresh';

  @observable public accessToken: string | null = null;
  @observable public refreshToken: string | null = null;

  constructor() {
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
}
