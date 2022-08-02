import { axiosInstance } from "../globals.js";
import jwt_decode from "jwt-decode";
import dayjs from "dayjs";

const setup = (store, router) => {
  axiosInstance.interceptors.request.use(
    (config) => {
      let token = localStorage.getItem("Token");

      if (token) {
        token = JSON.parse(token);
        const user = jwt_decode(token.refresh);
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;

        if (isExpired) {
          store.dispatch("userLogout").then(() => {
            router.push({ name: "login" });
          });
        }

        config.headers["Authorization"] = `Bearer ${token.access}`;
      }

      return config;
    },

    (error) => {
      return Promise.reject(error);
    }
  );

  axiosInstance.interceptors.response.use(
    (config) => {
      return config;
    },

    async (error) => {
      const originalConfig = error.config;
      console.log(originalConfig.url);
      if (error.response) {
        if (originalConfig.url !== "/login" && error.response.status === 401) {
          let token = localStorage.getItem("Token");
          if (token) {
            token = JSON.parse(token);
          }

          try {
            const rs = await axiosInstance.post("auth/jwt/refresh/", {
              refresh: token.refresh,
            });

            const { access } = rs.data;
            token.access = access;
            store.commit("updateStorage", token);
          } catch (_error) {
            return Promise.reject(_error);
          }
          return axiosInstance(originalConfig);
        }
      }
      return Promise.reject(error);
    }
  );
};

export default setup;
