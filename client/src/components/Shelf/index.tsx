import React from 'react';
import { useHistory } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { Card } from 'semantic-ui-react';

import { DrawSourceType as DrawSourceTypeEnum } from '../../interfaces/draw-source';
import { drawSourceTypes } from '../../constants';
import DrawSourceType from '../shared/DrawSourceType';

const Shelf: React.FC = observer(() => {
  const history = useHistory();

  const onChooseType = (type: DrawSourceTypeEnum) => history.push('/shelf/' + type);

  return (
    <Card.Group itemsPerRow={2}>
      {drawSourceTypes.map((item) => (
        <DrawSourceType key={item.type} onChoose={onChooseType} item={item} />
      ))}
    </Card.Group>
  );
});

export default Shelf;
