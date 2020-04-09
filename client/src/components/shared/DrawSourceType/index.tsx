import React from 'react';

import { StyledCard, StyledCardContent } from './styles';

type Props = { gradient: string };

const DrawSourceType: React.FC<Props> = ({ children, gradient }) => {
  return (
    <StyledCard gradient={gradient}>
      <StyledCardContent>{children}</StyledCardContent>
    </StyledCard>
  );
};

export default DrawSourceType;
