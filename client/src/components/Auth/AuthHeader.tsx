import React from 'react';
import { Header } from 'semantic-ui-react';

const AuthHeader: React.FC = ({ children }) => (
  <Header as="h1" textAlign="center" color="grey" style={{ marginBottom: '2rem' }}>
    {children}
  </Header>
);

export default AuthHeader;
