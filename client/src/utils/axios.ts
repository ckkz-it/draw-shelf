import axios from 'axios';

import { baseURL, storagePrefix } from '../config';
import { toSnakeCase } from './snake-case';
import { camelizeKeys } from './camel-case';

const axiosInstance = axios.create({ baseURL });
const accessToken = window.localStorage.getItem(storagePrefix + 'access');
axiosInstance.interceptors.request.use(
  (config) => ({
    ...config,
    headers: { ...config.headers, Authorization: `Bearer ${accessToken}` },
    data: config.data ? toSnakeCase(config.data) : config.data,
  }),
  (error) => {
    return Promise.reject(error);
  },
);

axiosInstance.interceptors.response.use(
  (response) => {
    if (response.data) {
      response.data = camelizeKeys(response.data);
    }
    return response;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export default axiosInstance;
