<script>
import swal from "sweetalert";
export default {
  props: {
    masterpassword: {
      default: "",
      type: String,
    },
  },

  data() {
    return {
      entrysite: "",
      entryemail: "",
      entrypassword: "",
    };
  },

  methods: {
    sendPostRequest(path, obj, callback) {
      this.$axios.post(path, obj).then(callback);
    },

    addNewEntry(e) {
      e.preventDefault();
      if (
        this.entrysite.trim() != "" &&
        this.entryemail.trim() != "" &&
        this.entrypassword.trim() != ""
      ) {
        const path = "/entries/new/";
        const obj = {
          entrysite: this.entrysite.trim(),
          entryemail: this.entryemail.trim(),
          entrypassword: this.entrypassword.trim(),
          masterpassword: this.masterpassword.trim(),
        };
        this.sendPostRequest(path, obj, (response) => {
          if (response.data.status == "ok") {
            this.entrysite = "";
            this.entryemail = "";
            this.entrypassword = "";
            swal("Entry Successfully Created");
          } else {
            let message = response.data.errors;
            swal("Please all ensure all fields have at maximum 70 chars");
          }
        });
      } else {
        swal("Plese, fill all the fields");
      }
    },
  },
};
</script>

<template>
  <div>
    <div class="form-group">
      <div><label for="masterpassword">Site</label></div>
      <input
        placeholder="Site"
        id="entrysite"
        v-model="entrysite"
        class="textinput textInput form-control"
        type="text"
        name="site"
        autocomplete="off"
      />
    </div>
    <div class="form-group">
      <div><label for="masterpassword">Email or Username</label></div>
      <input
        placeholder="Email"
        id="entryemail"
        v-model="entryemail"
        class="textinput textInput form-control"
        type="text"
        name="email"
        autocomplete="off"
      />
    </div>
    <div class="form-group">
      <div><label for="masterpassword">Password</label></div>
      <input
        placeholder="Password"
        id="entrypassword"
        v-model="entrypassword"
        class="textinput textInput form-control"
        type="text"
        name="password"
        autocomplete="off"
      />
    </div>
    <div>
      <button class="cta cta1" type="submit" @click="addNewEntry">
        Add <i class="fal fa-plus"></i>
      </button>
    </div>
  </div>
</template>
