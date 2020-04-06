import React from 'react';
import { observer } from 'mobx-react-lite';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';

import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import ProtectedRoute from './components/shared/ProtectedRoute';
import Shelf from './components/Shelf';
import PageWrapper from './components/PageWrapper';

const App: React.FC = observer(() => {
  return (
    <Router>
      <Switch>
        <Redirect exact from="/" to="/login" />
        <Route exact path="/login">
          <Login />
        </Route>
        <Route exact path="/sign-up">
          <Register />
        </Route>

        <PageWrapper>
          <ProtectedRoute exact path="/shelf">
            <Shelf />
          </ProtectedRoute>
        </PageWrapper>
      </Switch>
    </Router>
  );
});

export default App;
