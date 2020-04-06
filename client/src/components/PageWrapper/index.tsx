import React from 'react';
import { Container } from 'semantic-ui-react';

import PageHeader from './PageHeader';

const PageWrapper: React.FC = ({ children }) => {
  return (
    <Container>
      <PageHeader />
      {children}
    </Container>
  );
};

export default PageWrapper;
