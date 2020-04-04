import React from 'react';
import { Container, Segment } from 'semantic-ui-react';

const AuthWrapper: React.FC = ({ children }) => {
  return (
    <Container text className="centered-raised">
      <Segment raised>{children}</Segment>
    </Container>
  );
};

export default AuthWrapper;
