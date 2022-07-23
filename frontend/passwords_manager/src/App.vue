<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="bottom-nav">
      <div id="home" class="">
          <a href="/#/"><i class="fal fa-home"></i></a>
      </div>
      <div id="passwordGenerator" class="">
          <a href="/#/password-generator"><i class="fal fa-dice"></i></a>
      </div>
      <div id="info" class="">
          <a href="/#/info"><i class="fal fa-info"></i></a>
      </div>
      <div id="settings" class="">
          <a href="/#/settings"><i class="fal fa-cog"></i></a>
      </div>
  </div>
  <RouterView />
</template>

<style>
</style>
