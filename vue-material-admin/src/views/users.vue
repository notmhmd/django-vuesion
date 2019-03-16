<template>
  <div id="pageTable">
    <v-container grid-list-xl fluid>
      <v-snackbar
        :timeout="snackbar.timeout"
        :color="snackbar.color"
        :top="true"
        v-model="snackbar.state"
      >
        {{ snackbar.text }}
      </v-snackbar>
      <v-layout row wrap>
        <v-flex sm10>
          <h3>Users Info</h3>
        </v-flex>
        <v-flex sm2>
          <v-layout justify-start  fill-height>
            <v-dialog
              v-model="basic.newUser"
              persistent
              max-width="500px">
              <v-btn
                depressed
                icon
                fab
                small
                dark
                slot="activator"
                color="indigo">
                <v-icon dark>add</v-icon>
              </v-btn>
              <v-card>
                <v-card-title>
                  <span class="headline">Add New User</span>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-form ref="form" lazy-validation>
                    <v-container grid-list-md>
                      <v-layout wrap>
                        <v-flex xs8 sm6 md6>
                          <v-text-field
                            label="Username"
                            v-model="newUser.username"
                            required
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs8 sm6 md6>
                          <v-text-field
                            label="E-Mail"
                            :rule="rules.email"
                            v-model="newUser.email"
                            required
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs6>
                          <v-text-field
                            label="Password"
                            v-model="newUser.password1"
                            required
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs6>
                          <v-text-field
                            label="Password Confirmation"
                            v-model="newUser.password2"
                            required
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs12>
                          <v-text-field
                            label="Bio"
                            v-model="newUser.bio"
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs12>
                          <v-text-field
                            label="Photo"
                            v-model="newUser.photo"
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs8>
                          <v-select
                            v-model="select"
                            :items="userType"
                            item-text="type"
                            item-value="val"
                            label="User Type"
                            return-object
                            single-line
                          ></v-select>
                        </v-flex>
                      </v-layout>
                    </v-container>
                    <small>*indicates required field</small>
                  </v-form>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="blue darken-1"
                    flat
                    @click.native="basic.newUser = false"
                    >Close</v-btn>
                  <v-btn
                    color="blue darken-1"
                    flat
                    @click.native="addNewUser"
                    >Add</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-layout>
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
                      v-model="props.selected"
                    ></v-checkbox>
                  </td>
                  <td>
                    {{ props.item.id }}
                  </td>
                  <td>
                    <v-avatar size="32">
                      <img :src="props.item.photo" alt="" />
                    </v-avatar>
                  </td>
                  <td>{{ props.item.username }}</td>
                  <td>{{ props.item.email }}</td>
                  <td>{{ props.item.bio }}</td>
                  <td>
                    <v-dialog
                      v-model="basic.dialog"
                      persistent
                      max-width="500px">
                      <v-btn
                        depressed
                        outline
                        icon
                        fab
                        dark
                        slot="activator"
                        color="primary"
                        @click="getUserData(props.item.id)"
                        small>
                        <v-icon>edit</v-icon>
                      </v-btn>
                      <v-card>
                        <v-card-title>
                          <span class="headline">User Profile</span>
                        </v-card-title>
                        <v-divider></v-divider>
                        <v-card-text>
                          <v-form  ref="form" lazy-validation>
                            <v-container grid-list-md>
                              <v-layout wrap>
                                <v-flex xs8 sm6 md6>
                                  <v-text-field
                                    label="Legal first name"
                                    v-model="firstName"
                                    required
                                  ></v-text-field>
                                </v-flex>
                                <v-flex xs8 sm6 md6>
                                  <v-text-field
                                    label="Legal last name"
                                    required
                                    v-model="lastName"
                                  ></v-text-field>
                                </v-flex>
                                <v-flex xs12>
                                  <v-text-field
                                    label="Email"
                                    required
                                    :rules="[rules.required, rules.email]"
                                    v-model="userMail"
                                  ></v-text-field>
                                </v-flex>
                                <v-flex xs12>
                                  <v-text-field
                                    label="Username"
                                    required
                                    v-model="userName"
                                  ></v-text-field>
                                </v-flex>
                                <v-flex xs12>
                                  <v-text-field
                                    label="Password"
                                    type="password"
                                    required
                                  ></v-text-field>
                                </v-flex>
                                <v-flex xs12 sm6>
                                  <v-menu
                                    ref="menu"
                                    lazy
                                    class="pr-2"
                                    :close-on-content-click="false"
                                    v-model="menu"
                                    transition="scale-transition"
                                    offset-y
                                    full-width
                                    :nudge-bottom="-22"
                                    min-width="290px"
                                    :return-value.sync="date">
                                    <v-text-field
                                      slot="activator"
                                      label="End Date"
                                      v-model="date"
                                      append-icon="event"
                                      readonly
                                    ></v-text-field>
                                    <v-date-picker
                                      v-model="date"
                                      no-title
                                      scrollable>
                                      <v-spacer></v-spacer>
                                      <v-btn
                                        flat
                                        color="primary"
                                        @click="menu = false"
                                        >Cancel</v-btn>
                                      <v-btn
                                        flat
                                        color="primary"
                                        @click="$refs.menu.save(date)">OK</v-btn>
                                    </v-date-picker>
                                  </v-menu>
                                </v-flex>
                                <v-flex xs12 sm6>
                                  <v-text-field
                                    label="Location"
                                    v-model="userLocation"
                                  ></v-text-field>
                                </v-flex>
                                <v-flex xs12 sm6>
                                  <v-text-field
                                    label="Photo Link"
                                    v-model="userPhoto"
                                  ></v-text-field>
                                </v-flex>
                                <v-flex xs12 sm6>
                                  <v-text-field
                                    label="User Bio"
                                    v-model="userBio"
                                  ></v-text-field>
                                </v-flex>
                              </v-layout>
                            </v-container>
                            <small>*indicates required field</small>
                          </v-form>
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                            color="blue darken-1"
                            flat
                            @click.native="basic.dialog = false"
                            >Close</v-btn>
                          <v-btn
                            color="blue darken-1"
                            flat
                            @click.native="updateUser()"
                            >Save</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                    <v-dialog v-model="basic.deleteDialog" max-width="350px">
                      <v-btn
                        depressed
                        outline
                        icon
                        fab
                        @click="current = props.item.id"
                        dark
                        slot="activator"
                        color="pink"
                        small>
                        <v-icon>delete</v-icon>
                      </v-btn>
                      <v-card>
                        <v-card-title>
                          <span class="headline">User Delete</span>
                        </v-card-title>
                        <v-divider></v-divider>
                        <v-card-text>
                          Are You Sure You Want To Delete This User ?
                          <v-spacer></v-spacer>
                          <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                              color="blue darken-1"
                              flat
                              @click.native="basic.deleteDialog = false"
                              >Close</v-btn>
                            <v-btn
                              color="blue darken-1"
                              flat
                              @click.native="deleteUser(props.item.id)"
                              >Delete</v-btn>
                          </v-card-actions>
                        </v-card-text>
                      </v-card>
                    </v-dialog>
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
import VDialog from "vuetify/lib/components/VDialog/VDialog";

export default {
  components: {
    VDialog
  },
  data() {
    return {
      rules: {
        required: value => !!value || "Required.",
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return pattern.test(value) || "Invalid e-mail.";
        },
      },

      basic: {
        dialog: false,
        deleteDialog: false,
        newUser: false
      },
     newUser: {
        username: "",
        password1: "",
        password2: "",
        email: "",
        bio: "",
        photo: "",
        is_staff: false,
        is_moderator: false,
    },
      select: {
        type: "User",
        val: 0
      },
      userType: [
          { type: "User", val: 0 },
          { type: "Moderator", val: 1 },
          { type: "Admin", val: 2 }
      ],
      usersData: null,
      date: "",
      menu: false,
      firstName: "",
      lastName: "",
      userBio: "",
      userName: "",
      userLocation: "",
      userPhoto: "",
      userMail: "",
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
            text: "Avatar",
            value: "photo"
          },
          {
            text: "Username",
            value: "username"
          },
          {
            text: "Email",
            value: "email"
          },
          {
            text: "Bio",
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
    getUserData(userID) {
      let userDetail;
      axios
        .get("/api/user/" + userID)
        .then(response => {
          userDetail = response.data;
        })
        .finally(() => {
          this.firstName = userDetail.first_name;
          this.lastName = userDetail.last_name;
          this.userBio = userDetail.bio;
          this.userLocation = userDetail.location;
          this.userPhoto = userDetail.photo;
          this.endDate = userDetail.birth_date;
          this.userMail = userDetail.email;
          this.userName = userDetail.username;
        });

      console.error(userID);
      this.current = userID;
    },

    updateUser() {
      axios
        .put(
          "api/user/" + this.current,
          {
            first_name: this.firstName,
            last_name: this.lastName,
            username: this.userName,
            location: this.userLocation,
            email: this.userMail,
            bio: this.userBio,
            photo: this.userPhoto
          },
          {
            headers: {
              "X-CSRFToken": this.readCookie("csrftoken")
            }
          }
        )
        .then(() => {
          this.basic.dialog = false;
        })
        .then(() => {
          this.snackbar.state = true;
          this.snackbar.text = "Data Updated Succesfully";
          this.snackbar.color = "success";
        })
        .finally(() => {
          this.getUserList();
        });
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

    getUserList() {
      console.log(this.readCookie("csrftoken"));
      let testDump;
      axios
        .get("/api/user/")
        .then(response => {
          testDump = response.data;
        })
        .finally(() => {
          this.complex.items = testDump;
        });
    },

    deleteUser() {
      axios.delete("api/user/" + this.current)
          .then(res => { console.log(res) });
      this.basic.deleteDialog = false;
      this.getUserList();
    },

     addNewUser(event){
        if(this.select.val === 1){
            this.newUser.is_moderator = true;
        }else if(this.select.val === 2){
            this.newUser.is_staff = true;
        }
      axios.post("api/rest-auth/registration", this.newUser, {
          headers: {
              "X-CSRFToken": this.readCookie("csrftoken")
          }
      }).then((res) => {
          console.log(res);
          this.getUserList();
          this.basic.newUser = false;
          this.resetForm();
      });

     },
      resetForm(){
        this.newUser.username = "";
        this.newUser.password1 = "";
        this.newUser.password2 = "";
        this.newUser.email = "";
        this.newUser.bio = "";
        this.newUser.photo = "";
        this.newUser.is_staff = false;
        this.newUser.is_moderator = false;
      },

  },



  mounted() {
    this.getUserList();
  }
};
</script>
