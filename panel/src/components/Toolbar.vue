<template>
  <div>
    <md-toolbar class="md-accent">
      <h3 class="md-title">Simple PCA ImageNet Data Viewer</h3>
          <md-dialog :md-active.sync="showDialog">
            <md-dialog-title>Add new image</md-dialog-title>

            <form novalidate class="md-layout" @submit.prevent="validateImage">
              <md-card class="md-layout-item md-size-100 md-small-size-200">
                <md-card-header>
                  <div class="md-title">Image</div>
                </md-card-header>

                <md-card-content>
                  <div class="md-layout md-gutter">
                    <div class="md-layout-item md-small-size-100">
                      <md-field :class="getValidationClass('imageName')">
                        <label for="image-name">Image Name</label>
                        <md-input name="image-name" id="image-name" v-model="form.imageName" :disabled="sending" />
                        <span class="md-error" v-if="!$v.form.imageName.required">The image name is required</span>
                        <span class="md-error" v-else-if="!$v.form.imageName.minlength">Invalid image name</span>
                      </md-field>
                      <md-field :class="getValidationClass('imageFile')">
                        <label for="image">Image</label>
                        <md-file name="image" type="file" v-model="form.imageFile" accept="image/*" :disabled="sending" v-on:change="selectedFile($event)"/>
                        <span class="md-error" v-if="!$v.form.imageFile.required">The image is required</span>
                      </md-field>
                    </div>
                  </div>
                </md-card-content>

                <md-progress-bar md-mode="indeterminate" v-if="sending" />

                <md-card-actions>
                  <md-button class="md-raised" @click="showDialog = false" :disabled="sending">Close</md-button>
                  <md-button type="submit" class="md-raised md-accent" :disabled="sending">Upload image</md-button>
                </md-card-actions>
              </md-card>

              <md-snackbar :md-active.sync="imageSave">The image {{ lastImage }} was saved with success!</md-snackbar>

              <md-snackbar :md-duration="5000" :md-active.sync="showSnackbar" md-persistent>
                <span>Uploading image failed, due to: {{ error }}</span>
                <md-button class="md-primary" @click="showSnackbar = false">Ok :(</md-button>
              </md-snackbar>
            </form>
          </md-dialog>
      <div class="md-toolbar-section-end">
          <md-button class="md-icon-button" @click="showDialog = true">
            <md-icon>publish</md-icon>
          </md-button>
      </div>
    </md-toolbar>
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import {
  required,
  minLength
} from 'vuelidate/lib/validators'

export default {
  name: 'Toolbar',
  mixins: [validationMixin],
  data: () => ({
    showDialog: false,
    sending: false,
    form: {
      imageName: null,
      imageFile: null,
    },
    lastImage: "",
    image: null,
    imageSave: false,
    success: false,
    showSnackbar: false,
    error: null,
    imageFile: null,
  }),
  validations: {
    form: {
      imageName: {
        required,
        minLength: minLength(3)
      },
      imageFile: {
        required,
      }
    }
  },
  methods: {
    selectedFile(e) {
      this.file = e.target.files[0];
    },
    getValidationClass (fieldName) {
      const field = this.$v.form[fieldName]
      if (field) {
        return {
          'md-invalid': field.$invalid && field.$dirty
        }
      }
    },
    validateImage () {
      this.$v.$touch()

      if (!this.$v.$invalid) {
        console.log(this)
        this.sending = true;
        this.$parent.uploadImage(this.file, this.form.imageName)
        .then(resp => console.log(resp)).then(() => {
          this.imageSave = true;
        }).catch(e => {
          this.error = e;
          this.showSnackbar = true;
        }).then(() => {
          this.sending = false;
          this.showDialog = false;
          this.$parent.updateList();
        });
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .md-progress-bar {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
  }
</style>
