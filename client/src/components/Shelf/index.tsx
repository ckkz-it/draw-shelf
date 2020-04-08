import React, { useEffect } from 'react';
import { observer } from 'mobx-react-lite';

import { useStores } from '../../hooks/use-stores';

const Shelf: React.FC = observer(() => {
  const { drawSourceStore } = useStores();

  useEffect(() => {
    if (!drawSourceStore.drawSources) {
      drawSourceStore.fetchAll();
    }
  });

  if (!drawSourceStore.drawSources) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      {drawSourceStore.drawSources.map((item) => (
        <pre key={item.id}>{JSON.stringify(item, null, 2)}</pre>
      ))}
    </div>
  );
});

export default Shelf;
