import React from 'react';
import { Header, Icon, Modal } from 'semantic-ui-react';

import { IDrawSource } from '../../../interfaces/draw-source';
import { getTextColorBasedOnBg } from '../../../helpers/get-text-color-based-on-bg';

type Props = { drawSource: IDrawSource; opened: boolean; onClose: () => void };

const MarkerModal: React.FC<Props> = ({ drawSource, opened, onClose }) => {
  const color = drawSource.color;
  const backgroundColor = getTextColorBasedOnBg(drawSource.color);
  const contentColor = backgroundColor === 'black' ? '#cacaca' : '#4a4a4a';
  const dimmer = backgroundColor === 'white' ? 'inverted' : true;

  return (
    <Modal
      centered={false}
      size="tiny"
      closeIcon={<Icon name="close" style={{ color }} />}
      dimmer={dimmer}
      open={opened}
      onClose={onClose}
      style={{ backgroundColor, textAlign: 'center', fontSize: '1.5rem' }}
    >
      <Modal.Content style={{ color: contentColor, backgroundColor, padding: '2rem' }}>
        <Modal.Description>
          <Header as="h1" style={{ color, fontSize: '2rem' }}>
            {drawSource.name}
          </Header>
          <p>Company: {drawSource.company.name}</p>
          <p>Code: {drawSource.code}</p>
          <p>Color Code: {drawSource.color}</p>
          <p>Color Category: {drawSource.colorCategory}</p>
        </Modal.Description>
      </Modal.Content>
    </Modal>
  );
};

export default MarkerModal;
