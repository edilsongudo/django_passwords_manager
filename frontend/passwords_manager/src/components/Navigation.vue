<template>
  <div class="bottom-nav">
    <div id="home" class="">
      <router-link :to="{ name: 'home' }"
        ><i class="fal fa-home"></i
      ></router-link>
    </div>
    <div id="passwordGenerator" class="">
      <router-link to="/password-generator"
        ><i class="fal fa-dice"></i
      ></router-link>
    </div>
    <div id="info" class="">
      <router-link to="/info"><i class="fal fa-info"></i></router-link>
    </div>
    <div id="settings" class="">
      <router-link to="/settings"><i class="fal fa-cog"></i></router-link>
    </div>
  </div>
</template>
