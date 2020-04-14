import styled from 'styled-components';

export const StyledMarker = styled.div`
  &&& {
    border-radius: 10em;
    color: ${(props) => props.theme.color};
    background-color: ${(props) => props.theme.backgroundColor};
    padding: 10px 20px;
    cursor: pointer;

    &:hover {
    }
  }
`;
