import axios from "axios";

const getAPI = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
  timeout: 1000,
});

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

export { getAPI };
