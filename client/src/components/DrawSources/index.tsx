import React from 'react';
import { useParams, Redirect } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { Header } from 'semantic-ui-react';

import { useStores } from '../../hooks/use-stores';
import { useFetch } from '../../hooks/use-fetch';
import { DrawSourceType } from '../../interfaces/draw-source';
import { getComponentForDrawSource } from '../../helpers/get-component-for-ds';

const DrawSources: React.FC = observer(() => {
  const params = useParams<{ type: DrawSourceType }>();
  if (!params.type || !(params.type in DrawSourceType)) {
    return <Redirect to="/shelf" />;
  }
  const { drawSourceStore } = useStores();
  const { fetched } = useFetch(drawSourceStore.fetchAll);

  if (!fetched) {
    return <div>Loading...</div>;
  }

  const drawSources = drawSourceStore.drawSources.filter((ds) => ds.type === params.type);
  if (drawSources.length === 0) {
    return <Header as="h1">No {params.type + 's'} found</Header>;
  }

  const DSComponent = getComponentForDrawSource(params.type as DrawSourceType);

  return (
    <div style={{ display: 'flex', justifyContent: 'space-around' }}>
      {drawSources.map((ds) => (
        <DSComponent key={ds.id} drawSource={ds} />
      ))}
    </div>
  );
});

export default DrawSources;
