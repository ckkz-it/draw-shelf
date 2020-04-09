import React from 'react';
import { useParams, Redirect } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { Header } from 'semantic-ui-react';

import { useStores } from '../../hooks/use-stores';
import { useFetch } from '../../hooks/use-fetch';
import { DrawSourceType } from '../../interfaces/draw-source';
import { getComponentForDrawSource } from '../../helpers/get-component-for-ds';

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

  const drawSources = drawSourceStore.drawSources.filter((ds) => ds.type === type);
  if (drawSources.length === 0) {
    return <Header as="h1">No {type + 's'} found</Header>;
  }

  const DSComponent = getComponentForDrawSource(type as DrawSourceType);

  return (
    <div>
      {drawSources.map((ds) => (
        <DSComponent key={ds.type} drawSource={ds} />
      ))}
    </div>
  );
});

export default DrawSources;
