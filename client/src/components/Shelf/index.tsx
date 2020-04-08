import React from 'react';
import { observer } from 'mobx-react-lite';

import { useStores } from '../../hooks/use-stores';
import { useFetch } from '../../hooks/use-fetch';

const Shelf: React.FC = observer(() => {
  const { drawSourceStore } = useStores();

  const { error, fetched } = useFetch<void>(drawSourceStore.fetchAll);

  if (error) {
    return <div>{error?.message}</div>;
  }

  if (!fetched) {
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
