import axios from 'axios';

import { baseURL } from '../config';
import { toSnakeCase } from './snake-case';
import { camelizeKeys } from './camel-case';
import { storageService } from '../services/storage-service';

const getAccessToken = () => storageService.getItem('access');

const axiosInstance = axios.create({ baseURL });

axiosInstance.interceptors.request.use(
  (config) => {
    let headers = config.headers;
    const token = getAccessToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
    return {
      ...config,
      data: config.data ? toSnakeCase(config.data) : config.data,
      headers,
    };
  },
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
