import React from 'react';
import { Redirect, Route, RouteProps } from 'react-router-dom';

import { useStores } from '../../hooks/user-stores';

const ProtectedRoute: React.FC<RouteProps> = ({ children, ...rest }) => {
  const { authStore } = useStores();

  if (!authStore.isAuthenticated) {
    return <Redirect to="/login" />;
  }

  return <Route {...rest}>{children}</Route>;
};

export default ProtectedRoute;
