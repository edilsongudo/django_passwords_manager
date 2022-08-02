import router from "../router";
import { axiosInstance } from "../globals.js";
import store from "../store";

export const check_user_master_key_status = function () {
  if (store.getters.loggedIn) {
    axiosInstance.get("/master-key/status/").then((response) => {
      const status = response.data.has_user_defined_a_master_password;
      if (!status) {
        router.push("/master-key/new/");
      }
    });
  }
};
