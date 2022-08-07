<script>
import swal from "sweetalert";
export default {
  data() {
    return {
      uid: "",
      token: "",
      new_password: "",
      re_new_password: "",
    };
  },
  methods: {
    resetPassword() {
      if (this.new_password === this.re_new_password) {
        this.$axios
          .post("/auth/users/reset_password_confirm/", {
            uid: this.uid,
            token: this.token,
            new_password: this.new_password,
            re_new_password: this.re_new_password,
          })
          .then((response) => {
            if (response.status === 204) {
              this.$router.push({ name: "login" });
            }
          });
      } else {
        swal("Both fields must be equal");
      }
    },
  },
  created() {
    this.uid = this.$route.params.uid;
    this.token = this.$route.params.token;
  },
};
</script>

<template>
  <div class="container">
    <div class="fullwidth">
      <div>
        <h1>Reset Account Password</h1>
        <div class="form-group">
          <input
            type="password"
            name="new_password"
            id="id_new_password"
            v-model="new_password"
            class="textinput textInput form-control"
            placeholder="Type your new password"
          />
        </div>
        <div class="form-group">
          <input
            type="password"
            name="re_new_password"
            id="id_re_new_password"
            v-model="re_new_password"
            class="textinput textInput form-control"
            placeholder="Confirm your new password"
          />
        </div>
        <button @click="resetPassword" class="cta cta1">Reset</button>
      </div>
    </div>
  </div>
</template>
