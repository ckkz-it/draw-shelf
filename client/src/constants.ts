import {
  DrawSourceResource,
  DrawSourceResourceItem,
  DrawSourceType,
  DrawSourceTypeItem,
} from './interfaces/draw-source';

export const drawSourceTypes: DrawSourceTypeItem[] = [
  {
    type: DrawSourceType.marker,
    label: 'Markers',
    gradient: 'linear-gradient(150deg, rgba(84,202,204,1) 0%, rgba(255,234,188,1) 100%)',
  },
  {
    type: DrawSourceType.paints,
    label: 'Paints',
    gradient: 'linear-gradient(150deg, rgba(255,160,172,1) 0%, rgba(255,217,135,1) 100%)',
  },
];

export const drawSourceResourceOptions: DrawSourceResourceItem[] = [
  {
    value: DrawSourceResource.full,
    key: DrawSourceResource.full,
    text: 'Full',
  },
  {
    value: DrawSourceResource.half,
    key: DrawSourceResource.half,
    text: 'Half',
  },
  {
    value: DrawSourceResource.low,
    key: DrawSourceResource.low,
    text: 'Low',
  },
  {
    value: DrawSourceResource.empty,
    key: DrawSourceResource.empty,
    text: 'Empty',
  },
];
