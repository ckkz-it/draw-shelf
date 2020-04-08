import { action, observable } from 'mobx';

import { DrawSourceApi } from '../apis/draw-source-api';
import { IDrawSource } from '../interfaces/draw-source';

export class DrawSourceStore {
  @observable public drawSources: IDrawSource[] | null = null;

  constructor(private api: DrawSourceApi) {}

  @action setDrawSources(ds: IDrawSource[]) {
    this.drawSources = ds;
  }

  @action async fetchAll() {
    const ds = await this.api.getAll();
    this.setDrawSources(ds);
  }
}
