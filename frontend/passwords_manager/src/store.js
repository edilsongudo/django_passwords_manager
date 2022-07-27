import { createApp } from "vue";
import { createStore } from "vuex";
import getAPI from "./axios-api";

// Create a new store instance.
const store = createStore({
  state() {
    return {
      accessToken: localStorage.getItem("accessToken"),
      refreshToken: localStorage.getItem("refreshToken"),
      APIData: "",
    };
  },
  mutations: {
    updateStorage(state, { access, refresh }) {
      state.accessToken = access;
      state.refreshToken = refresh;
      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);
    },
    destroyToken(state) {
      state.accessToken = null;
      state.refreshToken = null;
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
    },
  },
  getters: {
    loggedIn(state) {
      return state.accessToken != null;
    },
  },
  actions: {
    userLogout(context) {
      if (context.getters.loggedIn) {
        context.commit("destroyToken");
      }
    },
    userLogin(context, usercredentials) {
      return new Promise((resolve, reject) => {
        getAPI
          .post("auth/jwt/create/", {
            username: usercredentials.username,
            password: usercredentials.password,
          })
          .then((response) => {
            context.commit("updateStorage", {
              access: response.data.access,
              refresh: response.data.refresh,
            });
            resolve();
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
  },
});

export default store;
