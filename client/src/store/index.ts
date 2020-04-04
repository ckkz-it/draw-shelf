import React from 'react';

import { AuthStore } from './auth-store';
import { AuthApi } from '../apis/auth-api';

const authApi = new AuthApi();

export const storesContext = React.createContext({
  authStore: new AuthStore(authApi),
});
