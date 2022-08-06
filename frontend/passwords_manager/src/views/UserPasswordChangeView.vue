<script>
import swal from "sweetalert";
export default {
  data() {
    return {
      new_password: "",
      re_new_password: "",
      current_password: "",
      authenticated: false,
    };
  },
  methods: {
    save() {
      if (this.new_password.trim() === this.re_new_password.trim()) {
        this.$axios
          .post("/auth/users/set_password/", {
            new_password: this.new_password,
            re_new_password: this.re_new_password,
            current_password: this.current_password,
          })
          .then(() => {
            this.$router.push({ name: "home" });
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        swal("Both fields must be equal");
      }
    },
    authenticate() {
      this.$axios
        .post("/user/password/check/", { password: this.current_password })
        .then((response) => {
          if (response.data.authenticated) {
            this.authenticated = true;
          } else {
            swal("Your password is wrong");
            this.password = "";
          }
        });
    },
  },
};
</script>

<template>
  <div class="container">
    <div class="fullwidth">
      <div method="POST">
        <div v-if="!authenticated">
          <h3>Confirm your identity</h3>
          <div class="form-group">
            <input
              autofocus
              autocomplete="off"
              type="text"
              name="current_password"
              id="id_current_password"
              v-model="current_password"
              class="textinput textInput form-control secret"
              placeholder="Your current password"
              maxlength="70"
            />
          </div>
          <button class="cta cta1" @click="authenticate" type="submit">
            Save
          </button>
        </div>

        <div v-else>
          <h3>Edit Account Login Password</h3>
          <div class="form-group">
            <input
              autofocus
              autocomplete="off"
              type="text"
              name="new_password"
              id="id_new_password"
              v-model="new_password"
              class="textinput textInput form-control secret"
              placeholder="Your new password"
              maxlength="70"
            />
          </div>
          <div class="form-group">
            <input
              autocomplete="off"
              type="text"
              name="re_new_password"
              id="id_re_new_password"
              v-model="re_new_password"
              class="textinput textInput form-control secret"
              placeholder="Confirm your new password"
              maxlength="70"
            />
          </div>
          <button class="cta cta1" @click="save" type="submit">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>
