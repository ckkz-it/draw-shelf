import React from 'react';
import { observer } from 'mobx-react-lite';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';

import Login from './components/Auth/Login';
import Register from './components/Auth/Register';

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
      </Switch>
    </Router>
  );
});

export default App;
