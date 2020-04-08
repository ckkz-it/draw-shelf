import axios from '../utils/axios';
import { IDrawSource } from '../interfaces/draw-source';

export class DrawSourceApi {
  async getAll(): Promise<IDrawSource[]> {
    const { data } = await axios.get('/draw_sources');
    return data;
  }
}
