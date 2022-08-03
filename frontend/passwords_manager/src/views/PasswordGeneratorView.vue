<script>
export default {
  data() {
    return {
      password: "",
    };
  },

  methods: {
    getrandompassword() {
      this.$axios.get("/password/generator/").then((response) => {
        this.password = response.data.password;
      });
    },
  },

  created() {
    this.getrandompassword();
  },
};
</script>

<template>
  <div class="container">
    <div class="fullwidth">
      <h3>Password Generator</h3>
      <p>Generate strong passwords</p>
      <div class="form-group">
        <input
          v-model="password"
          autofocus
          id="masterpassword"
          class="textinput textInput form-control"
          type="text"
          name="master"
          autocomplete="off"
        />
      </div>
      <div>
        <button @click="getrandompassword" class="cta cta1">
          Generate <i class="fal fa-dice"></i>
        </button>
      </div>
    </div>
  </div>
</template>
