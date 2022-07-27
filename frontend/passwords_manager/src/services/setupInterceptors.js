import getAPI from "../axios-api";

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

  async (error) => {
    const originalConfig = error.config;
    if (error.response.status === 401) {
      const refreshToken = localStorage.getItem("refreshToken")
      const rs = await getAPI.post("auth/jwt/refresh/", {refresh: refreshToken})
      const { access } = rs.data
      store.commit("updateStorage", {
        access: access,
        refresh: localStorage.getItem("refreshToken"),
      });
      return getAPI(originalConfig)
    } 
    return Promise.reject(error);
  })

}

export default setup