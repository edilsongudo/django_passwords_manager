import { getAPI } from "../axios-api";

const setup = (store) => {

  getAPI.interceptors.request.use(
  (config) => {
    let token = localStorage.getItem('accessToken');

    if (token) {
      config.headers['Authorization'] = `Bearer ${ token }`;
    }

    return config;
  }, 

  (error) => {
    return Promise.reject(error);
  })

getAPI.interceptors.response.use(
  (config) => {

    return config;
  }, 

  (error) => {
    return Promise.reject(error);
  })

}

export default setup