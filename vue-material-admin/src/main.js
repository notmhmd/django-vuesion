import Vue from "vue";
import "./plugins/vuetify";
import App from "./App.vue";
import router from "./router/";
import store from "./store";
import "./registerServiceWorker";
import "roboto-fontface/css/roboto/roboto-fontface.css";
import "font-awesome/css/font-awesome.css";
import axios from "axios";

Vue.config.productionTip = false;
Vue.prototype.$http = axios;
let token = localStorage.getItem("token");
if (token) {
  Vue.prototype.$http.defaults.headers.common["Authorization"] =
    "Token " + token;
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
