<script>
import store from "../store/";
export default {
  computed: {
    isloggedIn: function () {
      return this.$store.getters.loggedIn;
    },
  },
};
</script>

<template>
  <div v-if="isloggedIn" class="bottom-nav">
    <div id="home" class="">
      <router-link :to="{ name: 'home' }"
        ><i class="fal fa-door-closed"></i
      ></router-link>
    </div>
    <div id="passwordGenerator" class="">
      <router-link :to="{ name: 'password-generator' }"
        ><i class="fal fa-dice"></i
      ></router-link>
    </div>
    <div id="info" class="">
      <router-link :to="{ name: 'info' }"
        ><i class="fal fa-info"></i
      ></router-link>
    </div>
    <div id="settings" class="">
      <router-link :to="{ name: 'settings' }"
        ><i class="fal fa-cog"></i
      ></router-link>
    </div>
  </div>
</template>
