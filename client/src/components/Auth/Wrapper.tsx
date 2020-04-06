import React from 'react';
import { Container, Segment } from 'semantic-ui-react';
import styled from 'styled-components';

import { useStores } from '../../hooks/user-stores';
import { Redirect } from 'react-router-dom';

const StyledSegment = styled(Segment)`
  && {
    padding: 3rem 5rem;
    border-radius: 3%;
  }
`;

const AuthWrapper: React.FC = ({ children }) => {
  const { authStore } = useStores();

  if (authStore.isAuthenticated) {
    return <Redirect to="/shelf" />;
  }

  return (
    <Container text className="centered-raised">
      <StyledSegment raised>{children}</StyledSegment>
    </Container>
  );
};

export default AuthWrapper;
