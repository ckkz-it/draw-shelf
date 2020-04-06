import React from 'react';
import { Header } from 'semantic-ui-react';

export const AuthHeader: React.FC = ({ children }) => (
  <Header as="h1" textAlign="center" color="grey" style={{ marginBottom: '2rem' }}>
    {children}
  </Header>
);
