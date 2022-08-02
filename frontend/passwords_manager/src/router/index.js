import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import LogoutView from "../views/LogoutView.vue";
import RegisterView from "../views/RegisterView.vue";
import MasterKeyNewView from "../views/MasterKeyNewView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: { requiresLogin: true, requiresMasterKey: true },
    },
    {
      path: "/master-key/new/",
      name: "master-new",
      component: MasterKeyNewView,
      meta: { requiresLogin: true },
    },
    {
      path: "/login/",
      name: "login",
      component: LoginView,
    },
    {
      path: "/logout/",
      name: "logout",
      component: LogoutView,
    },
    {
      path: "/register/",
      name: "register",
      component: RegisterView,
    },
  ],
});

export default router;
