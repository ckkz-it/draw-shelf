import React from 'react';

import { IDrawSource } from '../../../interfaces/draw-source';
import { StyledMarker } from './styles';
import { getTextColorBasedOnBg } from '../../../helpers/get-text-color-based-on-bg';

type Props = { drawSource: IDrawSource };

const Marker: React.FC<Props> = ({ drawSource }) => {
  return (
    <StyledMarker
      className="material-shadow"
      circular
      theme={{ backgroundColor: drawSource.color, color: getTextColorBasedOnBg(drawSource.color) }}
    >
      {drawSource.code}
    </StyledMarker>
  );
};

export default Marker;
