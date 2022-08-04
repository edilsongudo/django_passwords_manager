<script>
import swal from "sweetalert";
export default {
  data() {
    return {
      master: "",
      master_confirm: "",
      last_master: "",
    };
  },
  methods: {
    save() {
      if (this.master.trim() === this.master_confirm.trim()) {
        this.$axios
          .post("/master-key/edit/", {
            master: this.master,
            master_confirm: this.master_confirm,
            last_master: this.last_master,
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
  },
};
</script>


<template>
  <div class="container">
    <div class="fullwidth">
      <div method="POST">
        <h3>Edit master password</h3>
        <div class="alert alert-info">
          If your forget your master password you will never again be able to
          decrypt your encrypted passwords.
        </div>
        <div class="form-group">
          <input
            autofocus
            autocomplete="off"
            type="text"
            name="last_master"
            id="id_last_master"
            v-model="last_master"
            class="textinput textInput form-control secret"
            placeholder="Your current master password"
            maxlength="70"
          />
        </div>
        <div class="form-group">
          <input
            autofocus
            autocomplete="off"
            type="text"
            name="master"
            id="id_master"
            v-model="master"
            class="textinput textInput form-control secret"
            placeholder="Your new master password"
            maxlength="70"
          />
        </div>
        <div class="form-group">
          <input
            autocomplete="off"
            type="text"
            name="master_confirm"
            id="id_master_confirm"
            v-model="master_confirm"
            class="textinput textInput form-control secret"
            placeholder="Confirm your new master password"
            maxlength="70"
          />
        </div>
        <button class="cta cta1" @click="save" type="submit">Save</button>
      </div>
    </div>
  </div>
</template>