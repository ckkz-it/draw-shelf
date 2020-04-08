let BASE_URL = '';
if (process.env.NODE_ENV !== 'production') {
  BASE_URL = process.env.REACT_APP_BASE_URL!;
}

export const baseURL = BASE_URL;
export const storagePrefix: string = process.env.REACT_APP_STORAGE_PREFIX!;
export const jwtSecret: string = process.env.REACT_APP_JWT_SECRET!;
