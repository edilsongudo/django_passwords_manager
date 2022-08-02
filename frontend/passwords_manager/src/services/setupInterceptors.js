import { axiosIntance } from "../globals.js";
import jwt_decode from "jwt-decode";
import dayjs from "dayjs";

const setup = (store, router) => {
  axiosIntance.interceptors.request.use(
    (config) => {
      let token = localStorage.getItem("accessToken");

      if (token) {
        const user = jwt_decode(localStorage.getItem("refreshToken"));
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;

        if (isExpired) {
          store.dispatch("userLogout").then(() => {
            router.push({ name: "login" });
          });
        }

        config.headers["Authorization"] = `Bearer ${token}`;
      }

      return config;
    },

    (error) => {
      return Promise.reject(error);
    }
  );

  axiosIntance.interceptors.response.use(
    (config) => {
      return config;
    },

    async (error) => {
      const originalConfig = error.config;
      console.log(originalConfig.url);
      if (error.response) {
        if (originalConfig.url !== "/login" && error.response.status === 401) {
          const refreshToken = localStorage.getItem("refreshToken");

          try {
            const rs = await axiosIntance.post("auth/jwt/refresh/", {
              refresh: refreshToken,
            });

            const { access } = rs.data;
            store.commit("updateStorage", {
              access: access,
              refresh: localStorage.getItem("refreshToken"),
            });
          } catch (_error) {
            return Promise.reject(_error);
          }
          return axiosIntance(originalConfig);
        }
      }
      return Promise.reject(error);
    }
  );
};

export default setup;
