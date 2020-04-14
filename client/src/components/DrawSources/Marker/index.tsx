import React, { useState } from 'react';

import { DrawSourceResource, IDrawSource } from '../../../interfaces/draw-source';
import { StyledMarker } from './styles';
import { getTextColorBasedOnBg } from '../../../helpers/get-text-color-based-on-bg';
import MarkerModal from './Modal';
import { useStores } from '../../../hooks/use-stores';

type Props = { drawSource: IDrawSource };

const Marker: React.FC<Props> = ({ drawSource }) => {
  const [modalOpened, setModalOpened] = useState(false);
  const [modalDimmed, setModalDimmed] = useState(false);
  const [loadingUpdateRequest, setLoadingUpdateRequest] = useState(false);

  const { drawSourceStore } = useStores();

  const onSaveMarker = async (quantity: number, resource: DrawSourceResource) => {
    setModalDimmed(true);
    setLoadingUpdateRequest(true);
    await drawSourceStore.update(drawSource.id, { ...drawSource, quantity, resource });
    setLoadingUpdateRequest(false);
    setTimeout(() => setModalDimmed(false), 1500);
  };

  return (
    <>
      <StyledMarker
        className="material-shadow"
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
        onSave={onSaveMarker}
        dimmed={modalDimmed}
        loading={loadingUpdateRequest}
      />
    </>
  );
};

export default Marker;
