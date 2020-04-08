import { storagePrefix } from '../config';

class StorageService implements Storage {
  private storage = window.localStorage;
  private prefix = storagePrefix || '';

  public get length() {
    return this.storage.length;
  }

  public clear(): void {
    this.storage.clear();
  }

  public getItem<T = any>(key: string): T | null {
    try {
      return JSON.parse(this.storage.getItem(this.prefix + key));
    } catch {
      return null;
    }
  }

  public removeItem(key: string): void {
    this.storage.removeItem(this.prefix + key);
  }

  public setItem(key: string, value: any): void {
    this.storage.setItem(this.prefix + key, JSON.stringify(value));
  }

  public key(index: number): string | null {
    return this.storage.key(index);
  }
}

export const storageService = new StorageService();
