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
import UserEmailChangeView from "../views/UserEmailChangeView.vue";
import UserPasswordChangeView from "../views/UserPasswordChangeView.vue";

import store from "../store";
import { check_user_master_key_status } from "../helpers/";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: { requiresLogin: true, category: "home" },
    },
    {
      path: "/master-key/new/",
      name: "master-new",
      component: MasterKeyNewView,
      meta: { requiresLogin: true, category: "settings" },
    },
    {
      path: "/master-key/edit/",
      name: "master-edit",
      component: MasterKeyEditView,
      meta: { requiresLogin: true, category: "settings" },
    },
    {
      path: "/password/generator/",
      name: "password-generator",
      component: PasswordGeneratorView,
      meta: { requiresLogin: true, category: "password-generator" },
    },
    {
      path: "/info/",
      name: "info",
      component: InfoView,
      meta: { requiresLogin: true,category: "info" },
    },
    {
      path: "/settings/",
      name: "settings",
      component: SettingsView,
      meta: { requiresLogin: true, category: "settings" },
    },
    {
      path: "/user/email/change/",
      name: "email-change",
      component: UserEmailChangeView,
      meta: { requiresLogin: true, category: "settings" },
    },
    {
      path: "/users/set_password/",
      name: "password-change",
      component: UserPasswordChangeView,
      meta: { requiresLogin: true, category: "settings" },
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

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresLogin)) {
    check_user_master_key_status();
  }
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

router.afterEach((to, from) => {
  const category = to.meta.category;

  if (category) {
    try {
      const homeNav = document.querySelector("#home");
      const passwordGeneratorNav = document.querySelector("#passwordGenerator");
      const infoNav = document.querySelector("#info");
      const settingsNav = document.querySelector("#settings");

      // handle Nav Element Active Colors
      if (category == "home") {
        homeNav.classList.add("bottom-nav-active");
      } else {
        homeNav.classList.remove("bottom-nav-active");
      }
      if (category == "password-generator") {
        passwordGeneratorNav.classList.add("bottom-nav-active");
      } else {
        passwordGeneratorNav.classList.remove("bottom-nav-active");
      }
      if (category == "info") {
        infoNav.classList.add("bottom-nav-active");
      } else {
        infoNav.classList.remove("bottom-nav-active");
      }
      if (category == "settings") {
        settingsNav.classList.add("bottom-nav-active");
      } else {
        settingsNav.classList.remove("bottom-nav-active");
      }
    } catch (err) {
      console.log(err);
    }
  }
});

export default router;
