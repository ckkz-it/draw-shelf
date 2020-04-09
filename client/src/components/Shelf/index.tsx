import React from 'react';
import { observer } from 'mobx-react-lite';
import { Card } from 'semantic-ui-react';

import DrawSourceType from '../shared/DrawSourceType';

const Shelf: React.FC = observer(() => {
  return (
    <Card.Group itemsPerRow={2}>
      <DrawSourceType gradient="linear-gradient(150deg, rgba(84,202,204,1) 0%, rgba(255,234,188,1) 100%)">
        Markers
      </DrawSourceType>
      <DrawSourceType gradient="linear-gradient(150deg, rgba(255,189,197,1) 0%, rgba(255,217,135,1) 100%)">
        Paints
      </DrawSourceType>
    </Card.Group>
  );
});

export default Shelf;
