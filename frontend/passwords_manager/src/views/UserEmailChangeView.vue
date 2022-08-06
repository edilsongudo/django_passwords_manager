<script>
import swal from "sweetalert";
export default {
  data() {
    return {
      email: "",
      password: "",
      authenticated: false,
    };
  },
  created() {
    this.$axios.get("/user/email/change").then((response) => {
      this.email = response.data.email;
    });
  },
  methods: {
    authenticate() {
      this.$axios
        .post("/user/password/check/", { password: this.password })
        .then((response) => {
          if (response.data.authenticated) {
            this.authenticated = true;
          } else {
            swal("Your password is wrong");
            this.password = "";
          }
        });
    },
    save() {
      this.$axios
        .post("/user/email/change/", {
          email: this.email,
        }) //
        .then(() => {
          this.$router.push({ name: "home" });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<template>
  <div class="container">
    <div class="fullwidth">
      <div method="POST">
        <div v-if="authenticated">
          <h3>Change Email</h3>
          <div class="form-group">
            <input
              autofocus
              autocomplete="off"
              type="text"
              name="email"
              id="id_email"
              v-model="email"
              class="textinput textInput form-control"
              placeholder="Your new Email"
              maxlength="70"
            />
            <button class="cta cta1" @click="save" type="submit">Save</button>
          </div>
        </div>
        <div v-else>
          <h3>Confirm your identity</h3>
          <div class="form-group">
            <input
              autofocus
              autocomplete="off"
              type="text"
              name="password"
              id="id_password"
              v-model="password"
              class="textinput textInput form-control secret"
              placeholder="Type your password"
              maxlength="70"
            />
            <button class="cta cta1" @click="authenticate" type="submit">
              Confirm
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
