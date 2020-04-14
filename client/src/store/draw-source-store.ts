import { action, observable } from 'mobx';

import { DrawSourceApi } from '../apis/draw-source-api';
import { IDrawSource } from '../interfaces/draw-source';

export class DrawSourceStore {
  @observable public drawSources: IDrawSource[] | null = null;

  constructor(private api: DrawSourceApi) {}

  @action setDrawSources = (ds: IDrawSource[]) => {
    this.drawSources = ds;
  };

  @action fetchAll = async () => {
    const ds = await this.api.getAll();
    this.setDrawSources(ds);
  };

  update = async (id: string, dsData: IDrawSource) => {
    const updatedDs = await this.api.update(id, dsData);
    const updatedDrawSources = this.drawSources.map((ds) =>
      ds.id === id ? { ...ds, ...updatedDs } : ds,
    );
    this.setDrawSources(updatedDrawSources);
  };
}
