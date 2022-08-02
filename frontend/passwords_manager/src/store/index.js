import { createStore } from "vuex";
import { axiosInstance } from "../globals.js";

// Create a new store instance.
const store = createStore({
  state() {
    return {
      Token: JSON.parse(localStorage.getItem("Token")),
      APIData: "",
    };
  },
  mutations: {
    updateStorage(state, data) {
      state.Token = data;
      localStorage.setItem("Token", JSON.stringify(data));
    },
    destroyToken(state) {
      state.Token = null;
      localStorage.removeItem("Token");
    },
  },
  getters: {
    loggedIn(state) {
      return state.Token != null;
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
        axiosInstance
          .post("auth/jwt/create/", {
            username: usercredentials.username,
            password: usercredentials.password,
          })
          .then((response) => {
            context.commit("updateStorage", response.data);
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
