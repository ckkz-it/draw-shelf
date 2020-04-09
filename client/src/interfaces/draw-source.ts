import { ICompany } from './company';

export enum DrawSourceType {
  marker = 'marker',
  paints = 'paints',
}

export interface IDrawSource {
  id: string;
  type: DrawSourceType;
  name: string;
  color: string;
  code: string;
  colorCategory: string;
  company: ICompany;
}

export type DrawSourceTypeItem = {
  type: DrawSourceType;
  label: string;
  gradient: string;
};
