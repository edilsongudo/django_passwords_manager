import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import router from "./router";
import { axiosInstance } from "./globals.js";

import "./assets/main.css";

import setupInterceptors from "./services/setupInterceptors";

setupInterceptors(store, router);

const app = createApp(App);

app.use(router);
app.use(store);

app.config.globalProperties.$axios = axiosInstance;

app.mount("#app");
