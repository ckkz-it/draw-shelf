import { action, observable } from 'mobx';

import { IUser } from '../interfaces/auth';

export class UserStore {
  @observable public user: IUser | null = null;

  @action setUser(user: IUser) {
    this.user = user;
  }
}
