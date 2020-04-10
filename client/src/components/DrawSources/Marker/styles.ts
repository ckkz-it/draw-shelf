import styled from 'styled-components';
import { Button, Header } from 'semantic-ui-react';

export const StyledMarker = styled(Button)`
  &&& {
    color: ${(props) => props.theme.color};
    background-color: ${(props) => props.theme.backgroundColor};
  }
`;

export const StyledModalHeader = styled(Header)`
  && {
    font-size: 2rem !important;
    margin-bottom: 2rem;
    padding: 0.5rem;
    border-radius: 10em;
    box-shadow: 0 10px 20px 5px rgba(${(props) => props.theme.borderColor}, 0.5);
  }
`;
