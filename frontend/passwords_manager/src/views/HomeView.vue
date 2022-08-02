<script>
import swal from "sweetalert";
import IdleJs from "idle-js";
import EntriesList from "@/components/EntriesList.vue";
import EntriesAdd from "@/components/EntriesAdd.vue";

export default {
  components: {
    EntriesList,
    EntriesAdd,
  },

  created() {
    var state = this;
    var idle = new IdleJs({
      idle: 1000 * 60 * 2, // idle time in ms
      onIdle: function () {
        state.authenticated = false;
        state.masterpassword = false;
        state.entries = [];
      },
    });
    idle.start();
  },

  data() {
    return {
      authenticated: false,
      masterpassword: false,
      show_list: true,
      entries: [],
    };
  },

  methods: {
    sendPostRequest(path, obj, callback) {
      this.$axios.post(path, obj).then(callback);
    },

    checkMasterPassword() {
      const masterpass = document.querySelector("#masterpassword");
      const obj = { masterpassword: masterpass.value.trim() };
      const path = "entries/";
      this.sendPostRequest(path, obj, (response) => {
        if (response.data.is_masterpass_correct === true) {
          this.entries = response.data.response;
          this.authenticated = true;
          this.masterpassword = obj["masterpassword"];
        } else {
          swal("Your master password is wrong. Try Again");
        }
      });
      masterpass.value = "";
    },

    toggleList() {
      if (this.show_list) {
        this.show_list = false;
      } else {
        this.show_list = true;
        const path = "entries/";
        const obj = { masterpassword: this.masterpassword.trim() };
        this.sendPostRequest(path, obj, (response) => {
          this.entries = response.data.response;
        });
      }
    },
  },
};
</script>

<template>
  <div class="container">
    <div class="fullwidth">
      <div class="quick-action">
        <button
          v-if="authenticated && !show_list"
          @click="toggleList"
          class="shortcut"
        >
          <i class="fal fa-list"></i>
        </button>
        <button
          v-if="authenticated && show_list"
          @click="toggleList"
          class="shortcut"
        >
          <i class="fal fa-plus"></i>
        </button>
      </div>

      <div v-if="authenticated && !show_list">
        <EntriesAdd :masterpassword="masterpassword" />
      </div>

      <div v-else-if="authenticated && show_list">
        <EntriesList :entries="entries" :masterpassword="masterpassword" />
      </div>

      <div v-else autocomplete="off">
        <h3>Unlock Vault</h3>
        <p>Access your encrypted passwords</p>
        <div class="form-group">
          <div><label for="masterpassword">Master Password</label></div>
          <input
            @input="oninput"
            placeholder="master password"
            autofocus
            id="masterpassword"
            class="textinput textInput form-control secret"
            type="text"
            name="master"
            value=""
          />
        </div>
        <div>
          <button class="cta cta1" @click="checkMasterPassword">
            Unlock <i class="fal fa-key"></i>
          </button>
        </div>
      </div>
      
    </div>
  </div>
</template>

<style></style>

