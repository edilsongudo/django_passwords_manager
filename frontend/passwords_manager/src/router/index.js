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

import store from "../store";
import { check_user_master_key_status } from "../helpers/";

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

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresMasterKey)) {
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
    const name = to.name

    try {
      const homeNav = document.querySelector('#home')
      const passwordGeneratorNav = document.querySelector('#passwordGenerator')
      const infoNav = document.querySelector('#info')
      const settingsNav = document.querySelector('#settings')

      // handle Nav Element Active Colors
      if (name == "home") {
          homeNav.classList.add('bottom-nav-active')

      } else {
          homeNav.classList.remove('bottom-nav-active')
      }
      if (name == "password-generator") {
          passwordGeneratorNav.classList.add('bottom-nav-active')
      } else {
          passwordGeneratorNav.classList.remove('bottom-nav-active')
      }
      if (name == "info") {
          infoNav.classList.add('bottom-nav-active')
      } else {
          infoNav.classList.remove('bottom-nav-active')
      }
      if (name == "settings") {
          settingsNav.classList.add('bottom-nav-active')
      } else {
          settingsNav.classList.remove('bottom-nav-active')
      }      
    } catch (err) {
      console.log(err)
    }

})

export default router;
