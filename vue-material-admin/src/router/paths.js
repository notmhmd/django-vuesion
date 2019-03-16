export default [
  {
    path: "*",
    meta: {
      public: true
    },
    redirect: {
      path: "/404"
    }
  },
  {
    path: "/404",
    meta: {
      public: true
    },
    name: "NotFound",
    component: () =>
      import(/* webpackChunkName: "routes" */
      `@/views/NotFound.vue`)
  },
  {
    path: "/403",
    meta: {
      public: true
    },
    name: "AccessDenied",
    component: () =>
      import(/* webpackChunkName: "routes" */
      `@/views/Deny.vue`)
  },
  {
    path: "/500",
    meta: {
      public: true
    },
    name: "ServerError",
    component: () =>
      import(/* webpackChunkName: "routes" */
      `@/views/Error.vue`)
  },
  {
    path: "/login",
    meta: {
      public: true
    },
    name: "Login",
    component: () =>
      import(/* webpackChunkName: "routes" */
      `@/views/Login.vue`)
  },
  {
    path: "/",
    meta: {},
    name: "Root",
    redirect: {
      name: "Dashboard"
    }
  },
  {
    path: "/dashboard",
    meta: {
      breadcrumb: true,
      public: false,
      requiresAuth: true
    },
    name: "Dashboard",
    component: () => import("@/views/Dashboard")
  },
  {
    path: "/users",
    meta: { breadcrumb: true },
    name: "users",
    component: () =>
      import(/* webpackChunkName: "routes" */
      `@/views/users.vue`)
  },
  {
    path: "/books",
    meta: { breadcrumb: true },
    name: "/library/booksApproval",
    component: () => import("@/views/library/booksApproval")
  },
  {
    path: "/management",
    meta: { breadcrumb: true },
    name: "/library/booksManagement",
    component: () => import("@/views/library/booksManagement")
  },


];
