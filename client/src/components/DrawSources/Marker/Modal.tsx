import React from 'react';
import { Icon, Modal } from 'semantic-ui-react';

import { IDrawSource } from '../../../interfaces/draw-source';
import { StyledModalHeader } from './styles';
import { hexToRgb } from '../../../helpers/get-text-color-based-on-bg';

type Props = { drawSource: IDrawSource; opened: boolean; onClose: () => void };

const MarkerModal: React.FC<Props> = ({ drawSource, opened, onClose }) => {
  const borderColorRGB = hexToRgb(drawSource.color);
  const borderColorString = `${borderColorRGB.r}, ${borderColorRGB.g}, ${borderColorRGB.b}`;

  return (
    <Modal
      centered={false}
      size="tiny"
      closeIcon={<Icon style={{ color: 'black' }} name="close" />}
      dimmer="inverted"
      open={opened}
      onClose={onClose}
      style={{ fontSize: '1.5rem' }}
    >
      <Modal.Content style={{ padding: '2rem' }}>
        <Modal.Description>
          <StyledModalHeader textAlign="center" theme={{ borderColor: borderColorString }}>
            {drawSource.name}
          </StyledModalHeader>
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
