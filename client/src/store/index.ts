import React from 'react';

import { AuthStore } from './auth-store';

export const storesContext = React.createContext({
  authStore: new AuthStore(),
});
