<script>
import swal from "sweetalert";
export default {
  data() {
    return {
      email: "",
    };
  },
  methods: {
    sendRecoveryLink() {
      this.$axios
        .post("/auth/users/reset_password/", {
          email: this.email,
        })
        .then((response) => {})
        .catch((err) => {
          if (err.response) {
            swal(err.response.data.email[0]);
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
        <div>
          <h3>Reset Password</h3>
          <div class="form-group">
            <input
              autofocus
              autocomplete="off"
              type="email"
              name="email"
              id="id_email"
              v-model="email"
              class="textinput textInput form-control"
              placeholder="Your account's email address"
              maxlength="70"
            />
          </div>
          <button class="cta cta1" @click="sendRecoveryLink" type="submit">
            Send reset link
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
