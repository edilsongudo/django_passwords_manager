import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresLogin)) {
    if (!store.getters.loggedIn) {
      next({ name: "login" });
    } else {
      next();
    }
  } else {
    next();
  }
});

app.use(router);
app.use(store);

app.mount("#app");
