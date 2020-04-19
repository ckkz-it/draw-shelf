import React, { useState } from 'react';
import { observer } from 'mobx-react-lite';

import { DrawSourceResource, IDrawSource } from '../../../interfaces/draw-source';
import { StyledMarker } from './styles';
import { getTextColorBasedOnBg } from '../../../helpers/get-text-color-based-on-bg';
import MarkerModal from './Modal';
import { useStores } from '../../../hooks/use-stores';
import { useFetch } from '../../../hooks/use-fetch';

type Props = { drawSource: IDrawSource };

const Marker: React.FC<Props> = observer(({ drawSource }) => {
  const [modalOpened, setModalOpened] = useState(false);
  const [modalDimmed, setModalDimmed] = useState(false);

  const { drawSourceStore } = useStores();
  const markerUpdate = useFetch<void>({
    fetchFn: drawSourceStore.update,
    immediate: false,
  });

  const onSaveMarker = async (quantity: number, resource: DrawSourceResource) => {
    setModalDimmed(true);
    await markerUpdate.makeRequest(drawSource.id, { ...drawSource, quantity, resource });
    setTimeout(() => setModalDimmed(false), markerUpdate.error ? 4000 : 2000);
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
        loading={markerUpdate.loading}
        error={!!markerUpdate.error}
      />
    </>
  );
});

export default Marker;
