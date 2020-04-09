import { FunctionComponent } from 'react';

import { DrawSourceType, IDrawSource } from '../interfaces/draw-source';
import Marker from '../components/DrawSources/Marker';

type CommonFCProps = { key: string | number; drawSource: IDrawSource };

type ComponentForTypeReference = {
  [key in DrawSourceType]: FunctionComponent<CommonFCProps>;
};

const compTypeRef: ComponentForTypeReference = {
  [DrawSourceType.marker]: Marker,
  [DrawSourceType.paints]: () => null,
};

export const getComponentForDrawSource = (
  dsType: DrawSourceType,
): FunctionComponent<CommonFCProps> => {
  return compTypeRef[dsType];
};
