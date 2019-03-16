<template>
  <div id="bookList">
    <v-container grid-list-xl fluid>
      <v-snackbar
        :timeout="snackbar.timeout"
        :color="snackbar.color"
        :top="true"
        v-model="snackbar.state">
        {{ snackbar.text }}
      </v-snackbar>
      <v-layout row wrap>
        <v-flex sm12>
          <h3>Book List</h3>
        </v-flex>
        <v-flex lg12>
          <v-card>
            <v-toolbar card color="white">
              <v-text-field
                flat
                solo
                prepend-icon="search"
                placeholder="Type something"
                v-model="search"
                hide-details
                class="hidden-sm-and-down"
              ></v-text-field>
              <v-btn icon>
                <v-icon>filter_list</v-icon>
              </v-btn>
            </v-toolbar>
            <v-divider></v-divider>
            <v-card-text class="pa-0">
              <v-data-table
                :headers="complex.headers"
                :search="search"
                :items="complex.items"
                :rows-per-page-items="[10, 25, 50, { text: 'All', value: -1 }]"
                class="elevation-1"
                item-key="name"
                select-all
                v-model="complex.selected">
                <template slot="items" slot-scope="props">
                  <td>
                    <v-checkbox
                      primary
                      hide-details
                      v-model="props.selected"></v-checkbox>
                  </td>
                  <td>{{ props.item.id }}</td>
                  <td>{{ props.item.title }}</td>
                  <td>{{ props.item.description }}</td>
                  <td>{{ props.item.author }}</td>
                  <td>{{ props.item.uploaded_by }}</td>
                  <td>
                    <v-switch
                        v-model="props.item.approved"
                        :label="props.item.approved ?  'Approved' : 'Unapproved'"
                        @change="approveBook(props.item.id, props.item.approved)"
                        style="margin: 0!important;"
                    ></v-switch>
                  </td>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  components: {
  },
  data() {
    return {
      switchMe: false,
      bookState: "Approved",
      basic: {
        dialog: false,
        deleteDialog: false
      },

      search: "",
      snackbar: {
        state: false,
        timeout: 2000,
        color: "",
        text: ""
      },
      current: 0,
      loading: true,
      complex: {
        selected: [],
        headers: [
          {
            text: "#",
            value: "id"
          },
          {
            text: "Title",
            value: "photo"
          },
          {
            text: "Description",
            value: "username"
          },
          {
            text: "Author",
            value: "email"
          },
          {
            text: "Uploaded By",
            value: "bio"
          },
          {
            text: "Action",
            value: ""
          }
        ],
        items: []
      }
    };
  },
  methods: {
    approveBook(bookID, stat){
       axios.post("api/book/approve/",{book_id: bookID},
           {
               headers: {
              "X-CSRFToken": this.readCookie("csrftoken")
           }})
           .then((res) => { console.log(res); stat ? this.bookState = "Approved" : this.bookState = "Unapproved" })
           .finally(() => { this.getBooksList() });

    },

    readCookie(name) {
      let nameEQ = name + "=";
      let ca = document.cookie.split(";");
      for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == " ") c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
      }
      return null;
    },

    getBooksList() {
      console.log(this.readCookie("csrftoken"));
      let testDump;
      axios
        .get("/api/book/approval/")
        .then(response => {
          testDump = response.data;
        })
        .finally(() => {
          this.complex.items = testDump;
        });
    },

  },

  mounted() {
    this.getBooksList();
  }
};
</script>
