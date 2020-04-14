import React, { useState } from 'react';
import {
  Button,
  Card,
  Dimmer,
  DropdownProps,
  Form,
  Header,
  Icon,
  InputOnChangeData,
  Loader,
  Modal,
} from 'semantic-ui-react';

import { DrawSourceResource, IDrawSource } from '../../../interfaces/draw-source';
import { drawSourceResourceOptions } from '../../../constants';

type Props = {
  drawSource: IDrawSource;
  opened: boolean;
  onClose: () => void;
  onSave: (quantity: number, resource: DrawSourceResource) => void;
  dimmed: boolean;
  loading: boolean;
};

const MarkerModal: React.FC<Props> = ({ drawSource, opened, onClose, onSave, dimmed, loading }) => {
  const [formData, setFormData] = useState({
    resource: drawSource.resource,
    quantity: drawSource.quantity,
  });

  const onFormSubmit = () => {
    onSave(formData.quantity, formData.resource);
  };

  const onQuantityChange = (
    event: React.ChangeEvent<HTMLInputElement>,
    { value }: InputOnChangeData,
  ) => {
    if (value === '') {
      setFormData((v) => ({ ...v, quantity: value as any }));
      return;
    }
    const quantity = parseInt(value, 10);
    if (!Number.isNaN(quantity)) {
      setFormData((v) => ({ ...v, quantity }));
    }
  };

  const onResourceChange = (event: React.SyntheticEvent<HTMLElement>, data: DropdownProps) => {
    setFormData((v) => ({ ...v, resource: data.value as DrawSourceResource }));
  };

  return (
    <Modal centered={false} size="tiny" basic closeIcon open={opened} onClose={onClose}>
      <Modal.Content style={{ padding: '2rem' }}>
        <Modal.Header>
          <Header
            as="h1"
            textAlign="center"
            style={{ marginBottom: '1rem', color: drawSource.color }}
          >
            {drawSource.name}
          </Header>
        </Modal.Header>
        <Dimmer.Dimmable dimmed={dimmed}>
          <Modal.Description>
            <Card fluid>
              <Card.Content>
                <Card.Header as="h3">{drawSource.company.name}</Card.Header>
              </Card.Content>
              <Card.Content style={{ fontSize: '1.1rem', color: '#000' }}>
                <div>Code - {drawSource.code}</div>
                <div>Color - {drawSource.color}</div>
                <div>Color Category - {drawSource.colorCategory}</div>
              </Card.Content>
              <Card.Content extra>
                <Form onSubmit={onFormSubmit}>
                  <Form.Field>
                    <Form.Input
                      name="quantity"
                      value={formData.quantity}
                      label="Quantity"
                      onChange={onQuantityChange}
                    />
                  </Form.Field>
                  <Form.Field>
                    <Form.Select
                      name="resource"
                      options={drawSourceResourceOptions}
                      value={formData.resource}
                      label="Resource"
                      onChange={onResourceChange}
                    />
                  </Form.Field>
                  <Button type="submit" fluid color="yellow" style={{ marginTop: '1rem' }}>
                    Save
                  </Button>
                </Form>
              </Card.Content>
            </Card>
          </Modal.Description>
          <Dimmer active={dimmed} inverted style={{ borderRadius: '0.3rem' }}>
            {loading ? (
              <Loader size="big" />
            ) : (
              <Header as="h3" icon style={{ color: '#000000', opacity: '0.85' }}>
                <Icon name="check" />
                Successfully updated!
              </Header>
            )}
          </Dimmer>
        </Dimmer.Dimmable>
      </Modal.Content>
    </Modal>
  );
};

export default MarkerModal;
