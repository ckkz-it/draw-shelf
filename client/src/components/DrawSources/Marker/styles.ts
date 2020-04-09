import styled from 'styled-components';
import { Button } from 'semantic-ui-react';

type Props = { bgColor?: string };

export const StyledMarker = styled(Button)<Props>`
  &&& {
    color: ${(props) => props.theme.color};
    background-color: ${(props) => props.theme.backgroundColor};

    &:hover {
      color: brighten();
    }
  }
`;

// export const StyledModalHeader
