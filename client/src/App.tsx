import React from 'react';
import { observer } from 'mobx-react-lite';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';

import './App.css';
import Login from './components/Login';
import Register from './components/Register';

const App: React.FC = observer(() => {
  return (
    <Router>
      <Switch>
        <Redirect exact from="/" to="/login" />
        <Route exact path="/login">
          <Login />
        </Route>
        <Route exact path="/register">
          <Register />
        </Route>
      </Switch>
    </Router>
  );
});

export default App;
