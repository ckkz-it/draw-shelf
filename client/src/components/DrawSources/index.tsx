import React from 'react';
import { useParams, Redirect } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { Header } from 'semantic-ui-react';

import { useStores } from '../../hooks/use-stores';
import { useFetch } from '../../hooks/use-fetch';
import { DrawSourceType } from '../../interfaces/draw-source';

const DrawSources: React.FC = observer(() => {
  const { type } = useParams<{ type: DrawSourceType }>();
  if (!type || !(type in DrawSourceType)) {
    return <Redirect to="/shelf" />;
  }
  const { drawSourceStore } = useStores();
  const { fetched } = useFetch(drawSourceStore.fetchAll);

  if (!fetched) {
    return <div>Loading...</div>;
  }

  const drawSources = drawSourceStore.drawSources
    .filter((ds) => ds.type === type)
    .map((ds) => <pre key={ds.id}>{JSON.stringify(ds, null, 2)}</pre>);

  if (drawSources.length === 0) {
    return <Header as="h1">No {type + 's'} found</Header>;
  }

  return <div>{drawSources}</div>;
});

export default DrawSources;
