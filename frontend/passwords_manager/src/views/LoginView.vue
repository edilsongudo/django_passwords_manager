<template>
  <div class="container">
    <div class="fullwidth">
      <form v-on:submit.prevent="login">
        <h1 class="">Log In</h1>
        <p v-if="incorrectAuth">
          Incorrect email or password entered - please try again
        </p>
        <div class="form-group">
          <input
            type="email"
            name="email"
            id="user"
            v-model="email"
            class="textinput textInput form-control"
            placeholder="email"
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
        <button type="submit" class="cta cta1">Login</button>
        <div>
          <router-link :to="{ name: 'register' }">
            Need an account?
          </router-link>
          <br />
          <router-link :to="{ name: 'password-forgot' }">
            Forgot Password?
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "login",
  data() {
    return {
      email: "",
      password: "",
      incorrectAuth: false,
    };
  },
  methods: {
    login() {
      this.$store
        .dispatch("userLogin", {
          email: this.email,
          password: this.password,
        })
        .then(() => {
          const searchParams = new URLSearchParams(window.location.search);
          if (searchParams.has("redirect")) {
            this.$router.push({ path: `${searchParams.get("redirect")}` });
          } else {
            this.$router.push({ name: "home" });
          }
        })
        .catch((err) => {
          console.log(err);
          this.incorrectAuth = true;
        });
    },
  },
};
</script>

<style></style>
