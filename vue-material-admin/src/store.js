import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    status: "",
    token: ""
  },
  mutations: {
    auth_request(state) {
      state.status = "loading";
    },

    auth_success(state, token) {
      state.status = "success";
      state.token = token;
    },

    auth_error(state) {
      state.status = "error";
    },

    logout(state) {
      state.status = "";
      state.token = "";
    },

    logged_out(state) {
      state.status = "logged_out";
    }
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit("auth_request");
        axios
          .post("/api/rest-auth/login/", user)
          .then(resp => {
            let token = resp.data.key;
            let user = resp.data.user;
            localStorage.setItem("token", token);
            axios.defaults.headers.common["Authorization"] = "Token " + token;
            commit("auth_success", token, user);
            resolve(resp);
          })
          .catch(err => {
            commit("auth_error");
            localStorage.removeItem("token");
            reject(err);
          })
          .finally(() => {
            axios
              .get("api/rest-auth/user/")
              .then(res =>
                localStorage.setItem("userDetail", JSON.stringify(res.data))
              );
          });
      });
    },

    logout({ commit }) {
      return new Promise(resolve => {
        commit("logout");
        axios
          .post("api/rest-auth/logout/")
          .then(res => {
            console.log(res.data);
            resolve(res);
          })
          .finally(() => {
            localStorage.removeItem("token");
            localStorage.removeItem("userDetail");
            delete axios.defaults.headers.common["Authorization"];
            commit("logged_out");
          });
      });
    }
  },

  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status
  },

  plugins:[createPersistedState()]
});
