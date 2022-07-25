<template>
  <div class="container">
    <div class="fullwidth">
      <form v-on:submit.prevent="register">
        <h1 class="">Register</h1>
        <div class="form-group">
          <input
            type="text"
            name="username"
            id="user"
            v-model="username"
            class="textinput textInput form-control"
            placeholder="Username"
          />
        </div>
        <div class="form-group">
          <input
            type="password"
            name="password"
            id="pass"
            v-model="password"
            class="textinput textInput form-control"
            placeholder="Password"
          />
        </div>
        <button type="submit" class="cta cta1">Register</button>
      </form>
    </div>
  </div>
</template>

<script>
import { getAPI } from "../axios-api";
export default {
  name: "register",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    register() {
      getAPI
        .post("auth/users/", {
          username: this.username,
          password: this.password,
        })
        .then(() => {
          this.$router.push({ name: "login" });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style></style>
