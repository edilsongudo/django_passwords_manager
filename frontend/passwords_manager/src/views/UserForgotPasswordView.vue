<script>
import swal from "sweetalert";
export default {
  data() {
    return {
      email: "",
      sent: false
    };
  },
  methods: {
    sendRecoveryLink() {
      this.$axios
        .post("/auth/users/reset_password/", {
          email: this.email,
        })
        .then((response) => {this.sent = true})
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
      <div v-if="!sent" method="POST">
        <div>
          <h3>Reset Password</h3>
          <div>After filling in the email you used to create your account, we'll send you an email with a link. Via this link you'll be able to reset your password.</div>
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
      <div v-else>
        <h3>Check your email inbox</h3>
        <p>An email with a link that allows you to reset your password was sent to your inbox</p>
      </div>
    </div>
  </div>
</template>
