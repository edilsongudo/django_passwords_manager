<script>
import swal from 'sweetalert';
import getAPI from "../axios-api";
import IdleJs from 'idle-js';

export default {
  created() {
    var state = this
    var idle = new IdleJs({
      idle: 30000, // idle time in ms
      onIdle: function () {
        state.authenticated = false;
        state.masterpassword = false;
        state.entries = [];
        swal(`Your were deauthenticated due to inativity.`);
      },
    });
    idle.start();
  },

  data() {
    return {
      authenticated: false,
      masterpassword: false,
      message: false,
      show_list: true,
      entrysite: "",
      entrypassword: "",
      entryemail: "",
      entries: [],
    };
  },

  methods: {

    show_alert: function (state, obj, timeout) {
      state.message = obj;
      setTimeout(function () {
        state.message = false;
      }, timeout);
    },

    sendPostRequest(path, obj, callback) {
      getAPI.post(path, obj).then(callback)
    },

    checkMasterPassword() {
      const masterpass = document.querySelector("#masterpassword");
      const obj = {masterpassword: masterpass.value.trim()};
      const path = ""
      this.sendPostRequest(path, obj, response=> {
        if (response.data.is_masterpass_correct === true) {
          this.entries = response.data.response;
          this.authenticated = true;
          this.masterpassword = obj["masterpassword"];
        } else {
          swal("Your master password is wrong. Try Again");
        }
      })
      masterpass.value = ""
    },

    listentries() {
      if (this.show_list) {
        this.show_list = false;
      } else {
        this.show_list = true;
        const path = ""
        const obj = { masterpassword: this.masterpassword.trim() }
        this.sendPostRequest(path, obj, response=> {
          this.entries = response.data.response;
        })
      }
    },

    addNewEntry(e) {
      e.preventDefault();
      if (
        this.entrysite.trim() != "" &&
        this.entryemail.trim() != "" &&
        this.entrypassword.trim() != ""
      ) {
        const path = "/new/";
        const obj = {
          entrysite: this.entrysite.trim(),
          entryemail: this.entryemail.trim(),
          entrypassword: this.entrypassword.trim(),
          masterpassword: this.masterpassword.trim(),
        }
        this.sendPostRequest(path, obj, response=> {
          if (response.data.status == "ok") {
            this.entrysite = "";
            this.entryemail = "";
            this.entrypassword = "";
            swal("Entry Successfully Created");
          } else {
            let message = response.data.errors;
            swal("Please all ensure all fields have at maximum 70 chars");
          }
        })
      } else {
        // swal("Plese, fill all the fields")
        this.show_alert(
          this,
          {
            message: "Plese, fill all the fields",
            class: "alert alert-danger",
          },
          3000
        );
      }
    },

    deleteEntry(e) {
      const id = e[0][0];
      swal({
        text: "Are you sure you want to delete?",
        buttons: true,
      }).then((willDelete) => {
        if (willDelete) {
          const path = "/delete/";
          const obj = { id: id };
          this.sendPostRequest(path, obj, response=> {
            const index = this.entries.findIndex(
              (item) => item["id"] == obj["id"]
            );
            this.entries.splice(index, 1);
          })
        } else {
        }
      });
    },
  },

};
</script>


<template>
  <div class="container">
    <div class="fullwidth">
      <div v-if="message" :class="message.class">{{ message.message }}</div>

      <div class="quick-action">
        <button
          v-if="authenticated && !show_list"
          @click="listentries"
          class="shortcut"
        >
          <i class="fal fa-list"></i>
        </button>
        <button
          v-if="authenticated && show_list"
          @click="listentries"
          class="shortcut"
        >
          <i class="fal fa-plus"></i>
        </button>
      </div>

      <div v-if="authenticated && !show_list">
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
      </div>

      <div v-else-if="authenticated && show_list">
        <div>
          <div class="form-group">
            <div class="entrycontainer" v-for="entry in entries">
              <div>
                <div class="entry-site">
                  <span class="entry-attribute">Site:</span> {{ entry.site }}
                </div>
                <div class="entry-email">
                  <span class="entry-attribute">User:</span> {{ entry.email }}
                </div>
                <div class="entry-password">
                  <span class="entry-attribute">Password:</span> {{
                  entry.decrypted_password }}
                </div>
                <button
                  :id="entry.site"
                  @click="deleteEntry(entry.id)"
                  class="update"
                >
                  <i class="fal fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <form v-else autocomplete="off">
        <!-- <div class="alert alert-info">Your vault can only be decrypted with your master password</div> -->
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
      </form>
    </div>
  </div>
</template>


<style></style>
