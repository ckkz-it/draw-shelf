import { ICompany } from './company';

export enum DrawSourceType {
  marker = 'marker',
  paints = 'paints',
}

export enum DrawSourceResource {
  empty = 'empty',
  low = 'low',
  half = 'half',
  full = 'full',
}

export interface IDrawSource {
  id: string;
  color: string;
  code: string;
  colorCategory: string;
  company: ICompany;
  name: string;
  quantity: number;
  resource: DrawSourceResource;
  type: DrawSourceType;
}

export type DrawSourceTypeItem = {
  type: DrawSourceType;
  label: string;
  gradient: string;
};

export type DrawSourceResourceItem = {
  key: string;
  value: DrawSourceResource;
  text: string;
};
