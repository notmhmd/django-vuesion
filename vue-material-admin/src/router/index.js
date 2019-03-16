import Vue from "vue";
import Router from "vue-router";
import paths from "./paths";
import store from "../store";
import NProgress from "nprogress";
import "nprogress/nprogress.css";

Vue.use(Router);
const router = new Router({
  base: "/",
  mode: "history",
  linkActiveClass: "active",
  routes: paths
});
// router gards
router.beforeEach((to, from, next) => {
  NProgress.start();
  let requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth) {
    if (store.getters.isLoggedIn) {
      next();
      return;
    }

    next("/login");
  } else {
    next();
    console.log("Working");
  }
});

router.afterEach((to, from) => {
  NProgress.done();
  console.log("transferee");
});

export default router;
