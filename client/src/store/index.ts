import React from 'react';

import { AuthStore } from './auth-store';
import { AuthApi } from '../apis/auth-api';
import { UserStore } from './user-store';
import { DrawSourceStore } from './draw-source-store';
import { DrawSourceApi } from '../apis/draw-source-api';

const authApi = new AuthApi();
const drawSourceApi = new DrawSourceApi();

const userStore = new UserStore();
const authStore = new AuthStore(authApi, userStore);
const drawSourceStore = new DrawSourceStore(drawSourceApi);

export const storesContext = React.createContext({
  authStore,
  userStore,
  drawSourceStore,
});
