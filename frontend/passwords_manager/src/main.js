import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import router from "./router";
import { axiosIntance } from './globals.js'

import "./assets/main.css";

import setupInterceptors from "./services/setupInterceptors";

setupInterceptors(store, router);

const app = createApp(App);

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresLogin)) {
    if (!store.getters.loggedIn) {
      next({ name: "login", query: { redirect: to.fullPath } });
    } else {
      next();
    }
  } else {
    next();
  }
});

app.use(router);
app.use(store);

app.config.globalProperties.$axios = axiosIntance;

app.mount("#app");
