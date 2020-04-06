import React from 'react';

import { AuthStore } from './auth-store';
import { AuthApi } from '../apis/auth-api';
import { UserStore } from './user-store';

const authApi = new AuthApi();

const userStore = new UserStore();
const authStore = new AuthStore(authApi, userStore);

export const storesContext = React.createContext({
  authStore,
  userStore,
});
