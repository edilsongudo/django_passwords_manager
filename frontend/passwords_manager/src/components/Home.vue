<template>
  <div class="container">
    <div class="fullwidth">
      <div v-if="message" :class="message.class">[[ message.message ]]</div>

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
                  <span class="entry-attribute">Site:</span> [[ entry.site ]]
                </div>
                <div class="entry-email">
                  <span class="entry-attribute">User:</span> [[ entry.email ]]
                </div>
                <div class="entry-password">
                  <span class="entry-attribute">Password:</span> [[
                  entry.decrypted_password ]]
                </div>
                <button
                  :id="entry.site"
                  @click="deleteEntry([[entry.id]])"
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
            class="textinput textInput form-control"
            type="text"
            name="master"
            value=""
          />
        </div>
        <div>
          <button class="cta cta1" type="submit" @click="checkMasterPassword">
            Unlock <i class="fal fa-key"></i>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { getAPI } from "../axios-api";
export default {
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

  delimiters: ["[[", "]]"],

  methods: {
    oninput: function (e) {
      if (e.target.value != "") {
        e.target.classList.add("secret");
      } else {
        e.target.classList.remove("secret");
      }
    },

    checkinativity: function () {
      var idleTime = 0;
      var state = this;
      $(document).ready(function () {
        // Increment the idle time counter every minute.
        var idleInterval = setInterval(timerIncrement, 1000); // 1 second

        // Reset the idle timer on user interaction
        $(this).mousemove(function (e) {
          idleTime = 0;
        });
        $(this).keypress(function (e) {
          idleTime = 0;
        });
        $(this).scroll(function (e) {
          idleTime = 0;
        });
      });

      function timerIncrement() {
        if (state.authenticated) {
          idleTime = idleTime + 1;
        }
        let maximumInativitySecondsAllowed = 60 * 2;
        if (idleTime > maximumInativitySecondsAllowed) {
          state.authenticated = false;
          state.masterpassword = false;
          state.entries = [];
          swal(`Your were deauthenticated due to inativity.`);
          idleTime = 0;
        }
      }
    },

    show_alert: function (state, obj, timeout) {
      state.message = obj;
      setTimeout(function () {
        state.message = false;
      }, timeout);
    },

    doAjaxPostMasterPassword: function (path, obj) {
      let data = JSON.stringify(obj);

      var state = this;

      $.ajax({
        url: path,
        headers: { "X-CSRFToken": csrfToken },
        dataType: "json",
        data: obj,
        type: "post",
        success: function (response) {
          if (response["is_masterpass_correct"] == "true") {
            state.entries = response["response"];
            state.authenticated = true;
            state.masterpassword = obj["masterpassword"];
          } else {
            swal("Your master password is wrong. Try Again");
          }
        },
      });
    },

    doAjaxPostNewEntry: function (path, obj) {
      let data = JSON.stringify(obj);

      var state = this;

      $.ajax({
        url: path,
        headers: { "X-CSRFToken": csrfToken },
        dataType: "json",
        data: obj,
        type: "post",
        success: function (response) {
          if (response["status"] == "ok") {
            state.entrysite = "";
            state.entryemail = "";
            state.entrypassword = "";
            swal("Entry Successfully Created");
          } else {
            let message = response["errors"];
            swal("Please all ensure all fields have at maximum 70 chars");
          }
        },
      });
    },

    doAjaxPostrequestEntries: function (path, obj) {
      let data = JSON.stringify(obj);

      var state = this;

      $.ajax({
        url: path,
        headers: { "X-CSRFToken": csrfToken },
        dataType: "json",
        data: obj,
        type: "post",
        success: function (response) {
          state.entries = response["response"];
        },
      });
    },

    doAjaxPostDeleteEntry: function (path, obj) {
      let data = JSON.stringify(obj);

      var state = this;

      $.ajax({
        url: path,
        headers: { "X-CSRFToken": csrfToken },
        dataType: "json",
        data: obj,
        type: "post",
        success: function (response) {
          let index = state.entries.findIndex(
            (item) => item["id"] == obj["id"]
          );
          state.entries.splice(index, 1);
        },
      });
    },

    checkMasterPassword: function (e) {
      e.preventDefault();
      let masterpass = document.querySelector("#masterpassword");
      this.doAjaxPostMasterPassword("", {
        masterpassword: masterpass.value.trim(),
      });
    },

    listentries: function () {
      if (this.show_list) {
        this.show_list = false;
      } else {
        this.show_list = true;
        this.doAjaxPostrequestEntries("", {
          masterpassword: this.masterpassword.trim(),
        });
      }
    },

    addNewEntry: function (e) {
      e.preventDefault();
      if (
        this.entrysite.trim() != "" &&
        this.entryemail.trim() != "" &&
        this.entrypassword.trim() != ""
      ) {
        let postData = {
          entrysite: this.entrysite.trim(),
          entryemail: this.entryemail.trim(),
          entrypassword: this.entrypassword.trim(),
          masterpassword: this.masterpassword.trim(),
        };
        this.doAjaxPostNewEntry("/new/", postData);
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

    deleteEntry: function (e) {
      const id = e[0][0];
      swal({
        text: "Are you sure you want to delete?",
        buttons: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.doAjaxPostDeleteEntry("/delete/", { id: id });
        } else {
        }
      });
    },
  },

  created() {
    this.checkinativity();
  },
};
</script>

<style></style>
