<script setup>
import { auth, db } from '../../firebase.js';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile } from "firebase/auth";
import { setDoc, doc, getDoc } from 'firebase/firestore';
import { Card, CardHeader, CardContent, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';
import { Textarea } from '@/components/ui/textarea';
import AuthenticationDialog from './AuthenticationDialog.vue';
import { ref as vueRef } from 'vue';
import ImageCropper from '../Supplier/ImageCropper.vue'
import 'vue-advanced-cropper/dist/style.css'
</script>

<!-- HTML STUFF -->
<template>
  <div class="mt-10 ">
    <!-- Login -->
    <Card class="mx-auto max-w-sm" v-if="isLogin">
      <CardHeader>
        <CardTitle class="text-2xl">
          Login 🔒
        </CardTitle>
        <CardDescription>
          Enter your email below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid gap-4">
          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input id="email" type="email" placeholder="name@example.com" required v-model="email" />
          </div>
          <div class="grid gap-2">
            <div class="flex items-center">
              <Label for="password">Password</Label>
            </div>
            <Input id="password" type="password" required v-model="password" />
          </div>
          <Button type="submit" class="w-full" @click="handleLogin">
            Login
          </Button>
          <Button variant="outline" class="w-full" @click="toggleLogin">
            Don't have an account? Sign up Now!
          </Button>
        </div>
      </CardContent>
    </Card>


    <!-- Sign Up -->
    <Tabs :default-value="isSupplier ? 'supplier' : 'account'" class="mx-auto max-w-sm" v-else>
      <TabsList class="grid w-full grid-cols-2">
        <TabsTrigger value="account" @click="toggleSupplier">
          Restaurant
        </TabsTrigger>
        <TabsTrigger value="supplier" @click="toggleSupplier">
          Supplier
        </TabsTrigger>
      </TabsList>
      <TabsContent value="account">
        <Card>
          <CardHeader>
            <CardTitle>Create Restaurant Account 🧑‍🍳</CardTitle>
            <CardDescription>
              Find Suppliers and Monitor your Orders
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-2">
            <div class="space-y-1">
              <Label for="name">Name</Label>
              <Input id="name" placeholder="Name" v-model="userName" />
            </div>

            <div class="space-y-1">
              <Label for="companyName">Company's Name</Label>
              <Input id="companyName" placeholder="Company Name" v-model="companyName" />
            </div>

            <div class="space-y-1">
              <Label for="companyAddress">Company's Address</Label>
              <Input id="companyAddress" placeholder="Company Address" v-model="companyAddress" />
            </div>

            <div class="space-y-1">
              <Label for="companyNumber">Company Number</Label>
              <Input type="tel" id="companyNumber" placeholder="Company Number" v-model="companyNumber" />
            </div>

            <div class="space-y-1">
              <Label for="email">Email</Label>
              <Input id="email" placeholder="name@example.com" v-model="email" />
            </div>

            <div class="space-y-1">
              <Label for="password">Password</Label>
              <Input id="password" type="password" v-model="password" />
            </div>

            <Button type="submit" class="w-full" @click="handleSignUp">
              Sign Up
            </Button>
            <Button variant="outline" class="w-full" @click="toggleLogin">
              Have an account? Log in Now!
            </Button>
          </CardContent>
        </Card>
      </TabsContent>

      <TabsContent value="supplier">
        <Card>
          <CardHeader>
            <CardTitle>Create Supplier Account 📦</CardTitle>
            <CardDescription>
              Find Restaurants and Manage your Inventory
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-2">
            <div class="space-y-1">
              <Label for="name">Name</Label>
              <Input id="name" placeholder="Name" v-model="userName" required
                :class="{ 'border-red-500': submitted && !userName }" />
            </div>

            <div class="space-y-1">
              <Label for="companyName">Company's Name</Label>
              <Input id="companyName" placeholder="Company Name" v-model="companyName" required
                :class="{ 'border-red-500': submitted && !companyName }" />
            </div>

            <div class="space-y-1">
              <Label for="companyAddress">Company's Address</Label>
              <Input id="companyAddress" placeholder="Company Address" v-model="companyAddress" required
                :class="{ 'border-red-500': submitted && !companyAddress }" />
            </div>

            <div class="space-y-1">
              <Label for="description">Company's Description</Label>
              <Textarea placeholder="Give a brief description about your company." v-model="companyDescription" required
                :class="{ 'border-red-500': submitted && !companyDescription }" />
            </div>

            <div class="space-y-1">
              <Label for="companyNumber">Company Number</Label>
              <Input type="tel" id="companyNumber" placeholder="Company Number" v-model="companyNumber" required
                :class="{ 'border-red-500': submitted && !companyNumber }" />
            </div>

            <div class="space-y-1">
              <Label for="email">Email</Label>
              <Input id="email" placeholder="name@example.com" v-model="email" required
                :class="{ 'border-red-500': submitted && !email }" />
            </div>

            <div class="space-y-1">
              <Label for="password">Password</Label>
              <Input id="password" type="password" v-model="password" required
                :class="{ 'border-red-500': submitted && !password }" />
            </div>

            <div class="space-y-1">
              <Label for="companyLogo">Company Logo</Label>
              <div class="space-y-2">
                <img v-if="imagePreview" :src="imagePreview" alt="Company Logo"
                  class="w-32 h-32 object-cover rounded-lg" />
                <input type="file" accept="image/*" @change="handleImageUpload" class="mt-1 block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100" />
              </div>
            </div>

            <Button type="submit" class="w-full" @click="handleSignUp">
              Sign Up
            </Button>
            <Button variant="outline" class="w-full" @click="toggleLogin">
              Have an account? Log in Now!
            </Button>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  </div>





  <!-- Sign In Success Dialog -->
  <AuthenticationDialog :showDialog="showAuthDialog" :status="statusHeader" :description="statusDescription"
    :success="statusSuccess" @update:showDialog="showAuthDialog = $event" />
  <div v-if="validationError" class="validation-error">
    {{ validationError }}
  </div>

  <!-- Cropper Dialog -->
  <div v-if="showCropper && selectedFile"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-4 rounded-lg max-w-2xl w-full">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Crop Image</h3>
        <button @click="cancelCrop" class="text-gray-500 hover:text-gray-700">
          Cancel
        </button>
      </div>
      <div class="mb-4">
        <ImageCropper :image-file="selectedFile" @crop-complete="handleCropComplete"
          @cancel="() => showCropper = false" />
      </div>
      <div class="flex justify-end gap-2">
        <Button variant="outline" @click="cancelCrop">Cancel</Button>
        <Button @click="cropImage">Crop & Save</Button>
      </div>
    </div>
  </div>

</template>

<!-- VUE STUFF -->
<script>
export default {
  name: 'Authentication',
  data() {
    return {
      // For Inputs
      email: '',
      password: '',
      userName: '',
      isLogin: true,
      isSupplier: false,

      // Supplier Based
      companyName: '',
      companyDescription: '',
      companyAddress: '',
      companyNumber: '',

      // Dialog
      showAuthDialog: false,
      statusHeader: "",
      statusDescription: "",
      statusSuccess: true,

      submitted: false,
      validationError: "",
      imageData: null,
      imagePreview: null,
      imageSource: null,
      showCropper: false,
      selectedFile: null,
      imageFile: null,
    };
  },
  created() {
    // Handle route query parameters
    if (this.$route.query.signup === 'true') {
      this.isLogin = false;
      const type = this.$route.query.type;

      if (type === 'supplier') {
        this.isSupplier = true;
        // Need to wait for next tick to ensure tabs are mounted
        this.$nextTick(() => {
          // Find and click the supplier tab
          const supplierTab = document.querySelector('[value="supplier"]');
          if (supplierTab) {
            supplierTab.click();
          }
        });
      } else {
        this.isSupplier = false;
        this.$nextTick(() => {
          // Find and click the restaurant tab
          const restaurantTab = document.querySelector('[value="account"]');
          if (restaurantTab) {
            restaurantTab.click();
          }
        });
      }
    }
  },
  methods: {
    toggleLogin() {
      this.isLogin = !this.isLogin;
    },
    toggleSupplier() {
      this.isSupplier = !this.isSupplier;
    },
    addSessionCookie(uid, userName, userType, points) {
      sessionStorage.setItem('userType', userType);
      sessionStorage.setItem('userName', userName);
      sessionStorage.setItem('uid', uid);
      sessionStorage.setItem('points', points);
    },
    handleLogin() {
      signInWithEmailAndPassword(auth, this.email, this.password)
        .then((userCredential) => {
          // Set User Type
          const uid = userCredential.user.uid;

          // Enter database and find userType
          const docRef = doc(db, "users", uid);
          getDoc(docRef).then((docSnap) => {

            if (docSnap.exists()) {
              const userName = docSnap.data().userName;
              const userType = docSnap.data().userType;
              const points = docSnap.data().points;


              // Store user data in session storage
              this.addSessionCookie(uid, userName, userType, points);
            }
          });


          // alert("Signed In")
          this.statusHeader = "Successfully Logged In!";
          this.statusDescription = "Redirecting to home page in 2 seconds...";
          this.statusSuccess = true;
          this.showAuthDialog = true;


          // Automatically close the dialog after 2 seconds
          setTimeout(() => {
            this.showAuthDialog = false;
            this.$router.push('/');
          }, 2000);
        })
        .catch((error) => {
          // Wrong password
          // alert("Wrong Username/Password. Try Again!")

          this.statusHeader = "Log In Unsuccessful";
          this.statusDescription = "Wrong Username/Password. Try Again!";
          this.statusSuccess = false;
          this.showAuthDialog = true;
        });
    },
    handleSignUp() {
      if (!this.validateFields()) {
        return; // Stop if validation fails
      }

      createUserWithEmailAndPassword(auth, this.email, this.password)
        .then((userCredential) => {
          const user = userCredential.user;
          updateProfile(user, {
            displayName: this.userName
          })
            .catch((error) => {
              // Handle specific Firebase auth errors
              let errorMessage = "Error in Signing Up, Please Try Again!";
              if (error.code === 'auth/email-already-in-use') {
                errorMessage = "This email is already registered. Please use a different email or login.";
              } else if (error.code === 'auth/invalid-email') {
                errorMessage = "Invalid email format. Please check your email address.";
              } else if (error.code === 'auth/weak-password') {
                errorMessage = "Password is too weak. Please use a stronger password.";
              }

              this.statusHeader = "Signed Up Unsuccessful";
              this.statusDescription = errorMessage;
              this.statusSuccess = false;
              this.showAuthDialog = true;
            });

          // Store user data in Firestore
          setDoc(doc(db, "users", user.uid), {
            userName: this.userName,
            companyName: this.companyName,
            companyAddress: this.companyAddress,
            companyNumber: this.companyNumber,
            userType: this.isSupplier ? "supplier" : "restaurant",
            points: this.isSupplier ? null : 0,
            companyDescription: this.isSupplier ? this.companyDescription : null,
            imageData: this.isSupplier ? this.imageData : null,
          })
            .then(() => {
              // Create supplier listing if user is a supplier
              if (this.isSupplier) {
                return setDoc(doc(db, "supplierListing", user.uid), {
                  supplierName: this.companyName,
                  inventory: [],
                  // Add any other supplier-specific fields you need
                });
              }

              //Get current month and year
              const date = new Date();
              const month = date.getMonth() + 1;
              const year = date.getFullYear();
              const inventoryKey = `${year}-${month < 10 ? '0' + month : month}-05`;

              // Create inventory document if user is a restaurant and create a map objects of inventory lvels with YYYY-MM-05 as key
              return setDoc(doc(db, "inventoryLevels", user.uid), {
                currentInventoryLevel: {
                  [inventoryKey]: {
                    beforeOrder: {},
                  },
                },
              });
            })
            .then(() => {
              // Create restaurant document if user is NOT a supplier
              if (!this.isSupplier) {
                return setDoc(doc(db, "restaurant", user.uid), {
                  inventoryTypes: {},
                });
              }
              return Promise.resolve();
            })
            .then(() => {
              // Add session cookie
              this.addSessionCookie(
                user.uid,
                this.userName,
                this.isSupplier ? "supplier" : "restaurant",
                this.isSupplier ? null : 0
              );

              this.statusHeader = "Signed Up Successful!";
              this.statusDescription = "Redirecting to home page in 2 seconds...";
              this.statusSuccess = true;
              this.showAuthDialog = true;

              setTimeout(() => {
                this.showAuthDialog = false;
                this.$router.push('/');
              }, 2000);
            })
            .catch((error) => {
              console.error("Error adding document: ", error);
              this.statusHeader = "Sign Up Error";
              this.statusDescription = "Error creating account. Please try again.";
              this.statusSuccess = false;
              this.showAuthDialog = true;
            });
        })
        .catch((error) => {
          console.error("Error in Signing Up, Please Try Again!", error);
          this.statusHeader = "Signed Up Unsuccessful";
          this.statusDescription = "Error in Signing Up, Please Try Again!";
          this.statusSuccess = false;
          this.showAuthDialog = true;
        });
    },
    // Add this validation method
    validateFields() {
      const commonFields = {
        'Name': this.userName,
        'Email': this.email,
        'Password': this.password,
        "Company's Name": this.companyName,
        "Company's Address": this.companyAddress,
        "Company Number": this.companyNumber
      };

      // Add company description and logo for supplier
      if (this.isSupplier) {
        commonFields["Company's Description"] = this.companyDescription;
        // Check if imagePreview exists (which is set after successful crop)
        if (!this.imagePreview) {
          this.showValidationError('Company Logo', 'Please upload and crop a company logo');
          return false;
        }
      }

      // Check each field
      for (const [fieldName, value] of Object.entries(commonFields)) {
        if (!value || value.trim() === '') {
          this.showValidationError(fieldName);
          return false;
        }
      }

      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        this.showValidationError('Email', 'Please enter a valid email address');
        return false;
      }

      // Validate password length
      if (this.password.length < 6) {
        this.showValidationError('Password', 'Password must be at least 6 characters long');
        return false;
      }

      return true;
    },
    showValidationError(fieldName, customMessage = null) {
      this.validationError = customMessage || `${fieldName} is required`;
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.showCropper = true;
      }
    },

    handleCropComplete({ file, url }) {
      this.imageFile = file;
      this.imagePreview = url;

      // Convert to base64
      const reader = new FileReader();
      reader.onloadend = () => {
        this.imageData = reader.result; // This will be the base64 string
      };
      reader.readAsDataURL(file);

      this.showCropper = false;
    },

    cancelCrop() {
      this.showCropper = false;
      this.imageSource = null;
      // Reset file input
      const fileInput = document.getElementById('companyLogo');
      if (fileInput) fileInput.value = '';
    },

    cropImage() {
      this.showCropper = false;
    },
  },
  watch: {
    '$route.query': {
      handler(newQuery) {
        if (newQuery.type === 'supplier') {
          this.isSupplier = true;
          this.$nextTick(() => {
            const supplierTab = document.querySelector('[value="supplier"]');
            if (supplierTab) {
              supplierTab.click();
            }
          });
        } else if (newQuery.type === 'restaurant') {
          this.isSupplier = false;
          this.$nextTick(() => {
            const restaurantTab = document.querySelector('[value="account"]');
            if (restaurantTab) {
              restaurantTab.click();
            }
          });
        }
      },
      immediate: true
    }
  }
};

</script>

<!-- CSS STUFF -->
<style>
.login-container {
  width: 80%;
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.button-submit {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
}

.button-switch {
  width: 100%;
  padding: 10px;
  background-color: #ebebeb;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.validation-error {
  color: red;
  margin-top: 20px;
  text-align: center;
}

.image-preview {
  width: 96px;
  height: 96px;
  object-fit: cover;
}

.cropper-container {
  width: 100%;
  height: 400px;
}

/* Make sure the cropper is responsive */
@media (max-width: 640px) {
  .cropper-container {
    height: 300px;
  }
}
</style>