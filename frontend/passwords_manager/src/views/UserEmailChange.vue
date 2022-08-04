<script>
import swal from "sweetalert";
export default {
  data() {
    return {
      email: "",
    };
  },
  created() {
    this.$axios.get("/user/email/change").then(response=> {
      this.email = response.data.email
    })
  },
  methods: {
    save() {
      this.$axios
        .post("/user/email/change/", {
          email: this.email,
        })
        .then(() => {
          this.$router.push({ name: "home" });
        })
        .catch((err) => {
          console.log(err);
        });
      }
    },
  }
</script>


<template>
  <div class="container">
    <div class="fullwidth">
      <div method="POST">
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
        </div>
        <button class="cta cta1" @click="save" type="submit">Save</button>
      </div>
    </div>
  </div>
</template>