<template>
  <div id="booksManagement">
    <v-container grid-list-xl fluid>
      <v-snackbar
        :timeout="snackbar.timeout"
        :color="snackbar.color"
        :top="true"
        v-model="snackbar.state">
        {{ snackbar.text }}
      </v-snackbar>
      <v-layout row wrap>
        <v-flex sm10>
          <h3>Book List</h3>
            <v-spacer></v-spacer>
        </v-flex>
        <v-flex sm2>
          <v-layout justify-start  fill-height>
            <v-dialog
              v-model="basic.newBookDialog"
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
                  <span class="headline">Add New Book</span>
                </v-card-title>
                  <v-divider></v-divider>
                    <v-img
                        :src="getImage()"
                        aspect-ratio="3.2">
                    </v-img>
                <v-divider></v-divider>
                <v-card-text>
                  <v-form ref="form" lazy-validation>
                    <v-container grid-list-md>
                      <v-layout wrap>
                        <v-flex xs8 sm6 md6>
                          <v-text-field
                            label="Book Title"
                            v-model="book.title"
                            required
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs8 sm6 md6>
                          <v-text-field
                            label="Book Author"
                            required
                            v-model="book.author"
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs12>
                          <v-text-field
                            label="Book Description"
                            required
                            v-model="book.description"
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs12>
                          <v-layout justify-start row fill-height>
                            <v-container>
                              <file-pond
                              name="book_pdf"
                              ref="pond"
                              class-name="my-pond"
                              label-idle="Drop The Book PDF..."
                              accepted-file-types="application/pdf"
                              v-on:init="handleNewFilePondInit"/>
                            </v-container>
                          </v-layout>
                        </v-flex>
                        <v-flex xs12>
                          <vue-dropzone
                            ref="newBookDropZone"
                            id="1"
                            v-on:vdropzone-sending="sendingEvent"
                            label="Drop Book Cover Here To Upload"
                            @vdropzone-complete="afterComplete"
                            :options="dropzoneNewOptions"/>
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
                    @click.native="basic.newBookDialog = false"
                    >Close</v-btn>
                  <v-btn
                    color="blue darken-1"
                    flat
                    @click.native="addNewBook()"
                    >Save</v-btn>
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
                      v-model="props.selected"/>
                  </td>
                  <td>{{ props.item.id }}</td>
                  <td>{{ props.item.title }}</td>
                  <td>{{ props.item.description }}</td>
                  <td>{{ props.item.author }}</td>
                  <td>{{ props.item.uploaded_by }}</td>
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
                        @click="loadBookDetail(props.item.id)"
                        small>
                        <v-icon>edit</v-icon>
                      </v-btn>
                      <v-card>
                        <v-card-title>
                          <span class="headline">Edit Book Detail</span>
                        </v-card-title>
                          <v-divider></v-divider>
                            <v-img
                                :src="getImage()"
                                aspect-ratio="3.2">
                            </v-img>
                        <v-divider></v-divider>
                        <v-card-text>
                          <v-form ref="form" lazy-validation>
                            <v-container grid-list-md>
                              <v-layout wrap>
                                <v-flex xs8 sm6 md6>
                                  <v-text-field
                                    label="Book Title"
                                    v-model="book.title"
                                    required
                                  ></v-text-field>
                                </v-flex>
                                <v-flex xs8 sm6 md6>
                                  <v-text-field
                                    label="Book Author"
                                    required
                                    v-model="book.author"
                                  ></v-text-field>
                                </v-flex>
                                <v-flex xs12>
                                  <v-text-field
                                    label="Book Description"
                                    required
                                    v-model="book.description"
                                  ></v-text-field>
                                </v-flex>
                                <v-flex xs12>
                                  <v-layout justify-start row fill-height>
                                    <v-container>
                                      <file-pond
                                      name="book_pdf"
                                      ref="pond"
                                      class-name="my-pond"
                                      label-idle="Drop The Book PDF..."
                                      accepted-file-types="application/pdf"
                                      v-on:init="handleFilePondInit"/>
                                    </v-container>
                                  </v-layout>
                                </v-flex>
                                <v-flex xs12>
                                  <vue-dropzone
                                    id="2"
                                    ref="coverDropZone"
                                    label="Drop Book Cover Here To Upload"
                                    @vdropzone-complete="afterComplete"
                                    :options="dropzoneOptions"/>
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
                          <span class="headline">Book Delete</span>
                        </v-card-title>
                        <v-divider></v-divider>
                        <v-card-text>
                          Are You Sure You Want To Delete This Book ?
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
                              @click.native="deleteBook()"
                              >Delete</v-btn>
                          </v-card-actions>
                        </v-card-text>
                      </v-card>
                    </v-dialog>
                    <v-dialog v-model="basic.commentDialog" persistent max-width="600px" >
                      <v-btn
                        depressed
                        outline
                        icon
                        fab
                        dark
                        slot="activator"
                        color="blue"
                        @click.native="loadComment(props.item.id)"
                        small>
                        <v-icon>insert_comment</v-icon>
                      </v-btn>
                      <v-card>
                        <v-card-title>
                          Comments On This Book
                        </v-card-title>
                          <v-divider></v-divider>
                          <v-card-text>
                            <v-data-table
                              :headers="commentTable.headers"
                              :search="commentTable.search"
                              :items="commentTable.items"
                              :rows-per-page-items="[10, 25, 50, { text: 'All', value: -1 }]"
                              class="elevation-1"
                              item-key="name"
                              select-all
                              v-model="commentTable.selected">
                                <template slot="items" slot-scope="props">
                                    <td>
                                      <v-checkbox
                                        primary
                                        hide-details
                                        v-model="props.selected"/>
                                    </td>
                                    <td> {{ props.item.id }} </td>
                                    <td> {{ props.item.author}} </td>
                                    <td> {{ props.item.text}} </td>
                                    <td> {{ props.item.created_at}} </td>
                                    <td>
                                      <v-switch
                                          v-model="props.item.approved_comment"
                                          :label="props.item.approved_comment ?  'Approved' : 'Unapproved'"
                                          @change="approveComment(props.item.id, props.item.approved_comment)"
                                          style="margin: 0!important;">
                                      </v-switch>
                                    </td>
                                </template>
                            </v-data-table>
                          </v-card-text>
                        <v-card-actions>
                          <v-btn
                            flat
                            color="blue darken-1"
                            @click.native="basic.commentDialog = false">
                            Close
                          </v-btn>
                        </v-card-actions>
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
import vueFilePond, { setOptions } from 'vue-filepond';
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type/dist/filepond-plugin-file-validate-type.esm.js';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.esm.js';
import 'filepond/dist/filepond.min.css';
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css';
import vue2Dropzone from 'vue2-dropzone'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'
import VDataTable from "vuetify/lib/components/VDataTable/VDataTable";
import VCheckbox from "vuetify/lib/components/VCheckbox/VCheckbox";

const FilePond = vueFilePond( FilePondPluginFileValidateType, FilePondPluginImagePreview );



export default {
  components: {
      VCheckbox,
      VDataTable,
      VDialog,
    FilePond,
    vueDropzone: vue2Dropzone
  },
  data() {
    return {
      search: "",
      current: 0,
      dropzoneOptions: {
        url: () => { return "api/book/cover/" + this.current + "/pic/" },
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        method: "PUT",
        maxFiles: 1,
        headers: {
            "Authorization": axios.defaults.headers.common["Authorization"],
            "X-CSRFToken": this.readCookie("csrftoken"),
            },
      },

      dropzoneNewOptions: {
        url: () => { return "api/book/approval/" },
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        autoProcessQueue: false,
        uploadMultiple: true,
        method: "POST",
        maxFiles: 2,
        headers: {
            "Authorization": axios.defaults.headers.common["Authorization"],
            "X-CSRFToken": this.readCookie("csrftoken"),
            },
        params: {
              title: "",
              author: "",
              description: ""
        }
      },
      myFiles: [],
      basic: {
        dialog: false,
        newBookDialog: false,
        deleteDialog: false,
        commentDialog: false
      },
      snackbar: {
        state: false,
        timeout: 2000,
        color: "",
        text: ""
      },
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
      },

  commentTable: {
        search: '',
        selected: [],
        headers: [
          {
            text: "#",
            value: "id"
          },
          {
            text: "Wrote By",
            value: "author"
          },
          {
            text: "Text",
            value: "text"
          },
          {
            text: "Time",
            value: "created_at"
          },
          {
            text: "Action",
            value: ""
          }
        ],
        items: []
      },
      commentStat: 'Approved',
      switchMe: false,
      currentBook: 0,
      book: {
          title: '',
          description: '',
          author: '',
          link: '',
          approved_at: '',
          book_cover: ''
      },
    };
  },
  methods: {
    //fileAdded(file){
      //if(file.type === "image/jpeg"){
      //}
    //},

    afterComplete(file){
          console.log(file);
          this.basic.newBookDialog = false;
          this.getBookList();

      },

    getImage(){
        if(!this.book.book_cover){
            return "/static/book-cover-placeholder.png";
        }
        return this.book.book_cover
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

    getBookList() {
      console.log(this.readCookie("csrftoken"));
      let testDump;
      axios
        .get("/api/book/management/")
        .then(response => {
          testDump = response.data;
        })
        .finally(() => {
          this.complex.items = testDump;
        });
    },

    handleFilePondInit: function() {
      console.log('FilePond has initialized');
      setOptions({
          server: {
              url: "api/book/",
              process:{
                  url: "document/",
                  method: "POST",
                  headers: {
                  "Authorization": "Token f69b3b474c6c517a4c37cbc6965086a79174f672",
                  "X-CSRFToken": this.readCookie("csrftoken"),
                  "Content-Disposition": "attachment; filename=book.pdf",
                  "X-BookID": this.current
                  },
              },
              revert: {
                  url: "upload/",
                  method: "DELETE",
                  headers: {
                  "Authorization": "Token f69b3b474c6c517a4c37cbc6965086a79174f672",
                  "X-CSRFToken": this.readCookie("csrftoken"),
                  "Content-Disposition": "attachment; filename=book.pdf",
                  "X-BookID": ''
                  },
              }
          }
      })

    },


    handleNewFilePondInit: function() {
      console.log('FilePond has initialized');
      setOptions({
          server: {}
      })

    },

    loadBookDetail(bookID){
      let bookData = {};
      this.current = bookID;
      axios.get("api/book/management/" + bookID)
          .then(response => {  bookData = response.data  })
          .finally(() => {
              this.book.title = bookData.title;
              this.book.author = bookData.author;
              this.book.description = bookData.description;
              this.book.approved_at = bookData.approved_at;
              this.book.link = bookData.link;
              this.book.book_cover = "/uploads/" + bookData.book_cover;
              console.log(bookData);
          });
    },

      addNewBook(){
        this.dropzoneNewOptions.params.title = this.book.title;
        this.dropzoneNewOptions.params.author = this.book.author;
        this.dropzoneNewOptions.params.description = this.book.description;
        this.$refs.newBookDropZone.processQueue();
      },

    sendingEvent(file, xhr, formData) {
       if(file.type === "application/pdf"){
           formData.append('document', file);
       }
        formData.append('book_cover', file)
    },

    loadComment(book_id){
    this.currentBook = book_id;
    axios.get("api/book/comment/" + book_id).then((res) =>{
        console.log(res.data);
        this.commentTable.items = res.data;
      })
    },


    approveComment(comment_id, stat){
       axios.post("api/book/comment/approve",{comment_id: comment_id},
           {
               headers: {
              "X-CSRFToken": this.readCookie("csrftoken")
           }})
           .then((res) => { console.log(res); stat ? this.bookState = "Approved" : this.bookState = "Unapproved" })
           .finally(() => { this.loadComment(this.currentBook) });

    },

    deleteBook(){
        axios.delete("api/book/management/" + this.current)
            .then(res => console.log(res.data))
            .finally(() => {
                this.getBookList();
                this.basic.deleteDialog = false;
            })
    }
  },

  created() {
    this.getBookList();
  }
};
</script>
