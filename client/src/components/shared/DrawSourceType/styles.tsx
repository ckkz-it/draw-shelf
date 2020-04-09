import styled from 'styled-components';
import { Card } from 'semantic-ui-react';

type StyleCardProps = { gradient: string };

export const StyledCard = styled(Card)<StyleCardProps>`
  min-height: 200px !important;
  font-size: 3rem !important;
  color: #fff;
  line-height: 1;
  cursor: pointer;
  background: ${(props) => props.gradient} !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24) !important;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;

  &:hover {
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22) !important;
  }
`;

export const StyledCardContent = styled.div`
  margin-top: 1.5rem;
  margin-left: 0.5rem;
`;
