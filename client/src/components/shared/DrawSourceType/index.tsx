import React from 'react';

import { StyledCard, StyledCardContent } from './styles';
import {
  DrawSourceType as DrawSourceTypeEnum,
  DrawSourceTypeItem,
} from '../../../interfaces/draw-source';

type Props = {
  onChoose: (type: DrawSourceTypeEnum) => void;
  item: DrawSourceTypeItem;
};

const DrawSourceType: React.FC<Props> = ({ item, onChoose }) => {
  return (
    <StyledCard
      gradient={item.gradient}
      className="material-shadow with-hover"
      onClick={() => onChoose(item.type)}
    >
      <StyledCardContent>{item.label}</StyledCardContent>
    </StyledCard>
  );
};

export default DrawSourceType;
