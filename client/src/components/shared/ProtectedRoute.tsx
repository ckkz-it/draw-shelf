import React from 'react';
import { Redirect, Route, RouteProps } from 'react-router-dom';
import { observer } from 'mobx-react-lite';

import { useStores } from '../../hooks/use-stores';

const ProtectedRoute: React.FC<RouteProps> = observer(({ children, ...rest }) => {
  const { authStore } = useStores();

  if (!authStore.isAuthenticated) {
    return <Redirect to="/login" />;
  }

  return <Route {...rest}>{children}</Route>;
});

export default ProtectedRoute;
