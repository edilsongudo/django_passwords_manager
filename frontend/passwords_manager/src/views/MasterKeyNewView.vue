<template>
  <div class="container">
    <div class="fullwidth">
      <div method="POST">
        <h3>Define master</h3>
        <div class="alert-danger">
          <i class="fal fa-exclamation-triangle"></i> Memorize your key: If you
          forget your master password you will not be able to unlock your vault
          and see your encrypted data
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
            placeholder="Define a new master password"
            maxlength="70"
          />
        </div>
        <div class="form-group">
          <input
            autocomplete="off"
            type="text"
            name="master_confirm"
            id="pass"
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

<script>
import swal from "sweetalert";
export default {
  data() {
    return {
      master: "",
      master_confirm: "",
    };
  },
  methods: {
    save() {
      if (this.master.trim() === this.master_confirm.trim()) {
        this.$axios
          .post("/master-key/new/", {
            master: this.master,
            master_confirm: this.master_confirm,
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

<style></style>
