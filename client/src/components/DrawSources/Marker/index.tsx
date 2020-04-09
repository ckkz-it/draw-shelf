import React, { useState } from 'react';

import { IDrawSource } from '../../../interfaces/draw-source';
import { StyledMarker } from './styles';
import { getTextColorBasedOnBg } from '../../../helpers/get-text-color-based-on-bg';
import MarkerModal from './Modal';

type Props = { drawSource: IDrawSource };

const Marker: React.FC<Props> = ({ drawSource }) => {
  const [modalOpened, setModalOpened] = useState(false);

  return (
    <>
      <StyledMarker
        className="material-shadow"
        circular
        theme={{
          backgroundColor: drawSource.color,
          color: getTextColorBasedOnBg(drawSource.color),
        }}
        onClick={() => setModalOpened(true)}
      >
        {drawSource.code}
      </StyledMarker>
      <MarkerModal
        drawSource={drawSource}
        opened={modalOpened}
        onClose={() => setModalOpened(false)}
      />
    </>
  );
};

export default Marker;
