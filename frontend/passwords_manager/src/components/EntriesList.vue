<script>
import swal from "sweetalert";
export default {
  props: {
    entries: {
      default: [],
      type: Array,
    },
    masterpassword: {
      default: "",
      type: String,
    },
  },
  methods: {
    sendPostRequest(path, obj, callback) {
      this.$axios.post(path, obj).then(callback);
    },

    deleteEntry(id) {
      swal({
        text: "Are you sure you want to delete?",
        buttons: true,
      }).then((willDelete) => {
        if (willDelete) {
          const path = "/entries/delete/";
          const obj = { id: id };
          this.sendPostRequest(path, obj, (response) => {
            const index = this.entries.findIndex(
              (item) => item["id"] == obj["id"]
            );
            this.entries.splice(index, 1);
          });
        } else {
        }
      });
    },
  },
};
</script>

<template>
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
            <span class="entry-attribute">Password:</span>
            {{ entry.decrypted_password }}
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
</template>
