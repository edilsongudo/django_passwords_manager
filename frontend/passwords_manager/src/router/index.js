import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import LogoutView from "../views/LogoutView.vue";
import RegisterView from "../views/RegisterView.vue";
import MasterKeyNewView from "../views/MasterKeyNewView.vue";
import MasterKeyEditView from "../views/MasterKeyEditView.vue";
import PasswordGeneratorView from "../views/PasswordGeneratorView.vue";
import InfoView from "../views/InfoView.vue";
import SettingsView from "../views/SettingsView.vue";
import UserEmailChange from "../views/UserEmailChange.vue"

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
      path: "/master-key/edit/",
      name: "master-edit",
      component: MasterKeyEditView,
      meta: { requiresLogin: true },
    },
    {
      path: "/password/generator/",
      name: "password-generator",
      component: PasswordGeneratorView,
      meta: { requiresLogin: true },
    },
    {
      path: "/info/",
      name: "info",
      component: InfoView,
      meta: { requiresLogin: true },
    },
    {
      path: "/settings/",
      name: "settings",
      component: SettingsView,
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
    {
      path: "/user/email/change/",
      name: "email-change",
      component: UserEmailChange,
    },
  ],
});

export default router;
