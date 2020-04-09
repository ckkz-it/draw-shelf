import styled from 'styled-components';
import { Card } from 'semantic-ui-react';

type StyleCardProps = { gradient: string };

export const StyledCard = styled(Card)<StyleCardProps>`
  &&&&& {
    min-height: 200px;
    font-size: 4rem;
    color: #fff;
    line-height: 1;
    cursor: pointer;
    background: ${(props) => props.gradient};
  }
`;

export const StyledCardContent = styled.div`
  margin-top: 1.5rem;
  margin-left: 0.5rem;
`;
