const Menu = [
  { header: "Apps" },

  {
    title: "Dashboard",
    group: "apps",
    icon: "dashboard",
    name: "Dashboard"
  },

  {
    title: "Users",
    group: "apps",
    icon: "person",
    name: "users"
  },

  {
    title: "Library Management",
    group: "library",
    component: "library",
    icon: "library_books",
    items: [
        {
          name: "booksApproval",
          title: "Books Approval",
          component: "/library/booksApproval"
        },
        { name: "booksManagement",
          title: "Books Management",
          component: "/library/booksManagement"
        },
    ]
  },

];
// reorder menu
Menu.forEach(item => {
  if (item.items) {
    item.items.sort((x, y) => {
      let textA = x.title.toUpperCase();
      let textB = y.title.toUpperCase();
      return textA < textB ? -1 : textA > textB ? 1 : 0;
    });
  }
});

export default Menu;
