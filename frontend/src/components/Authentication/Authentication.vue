<script setup>
import Navbar from '../Navbar.vue';
import { auth, db } from '../../firebase.js';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile } from "firebase/auth";
import { setDoc, doc } from 'firebase/firestore';
import { Card, CardHeader, CardContent, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import AuthenticationDialog from './AuthenticationDialog.vue';
</script>

<!-- HTML STUFF -->
<template>
  <Navbar />

  <div class="mt-10">
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
    <Tabs default-value="account" class="mx-auto max-w-sm" v-else>
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

            <!-- New Company Name Field -->
            <div class="space-y-1">
              <Label for="company-name">Company's Name</Label>
              <Input id="company-name" placeholder="Company's Name" v-model="companyName" />
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
              <Input id="name" placeholder="Name" v-model="userName" />
            </div>

            <!-- New Company Name Field for Supplier -->
            <div class="space-y-1">
              <Label for="company-name">Company's Name</Label>
              <Input id="company-name" placeholder="Company's Name" v-model="companyName" />
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
    </Tabs>
  </div>





  <!-- Sign In Success Dialog -->
  <AuthenticationDialog :showDialog="showAuthDialog" :status="statusHeader" :description="statusDescription"
    :success="statusSuccess" @update:showDialog="showAuthDialog = $event" />


</template>

<!-- VUE STUFF -->
<script>
export default {
  name: 'Authentication',
  data() {
    return {
      email: '',
      password: '',
      userName: '',
      companyName: '', // New company's name field
      isLogin: true,
      isSupplier: false,

      // Dialog
      showAuthDialog: false,
      statusHeader: "",
      statusDescription: "",
      statusSuccess: true,
    };
  },
  methods: {
    toggleLogin() {
      this.isLogin = !this.isLogin;
    },
    toggleSupplier() {
      this.isSupplier = !this.isSupplier;
    },
    handleLogin() {
      signInWithEmailAndPassword(auth, this.email, this.password)
        .then((userCredential) => {
          this.statusHeader = "Logged In Successful!";
          this.statusDescription = "Redirecting to home page in 2 seconds...";
          this.statusSuccess = true;
          this.showAuthDialog = true;

          setTimeout(() => {
            this.showAuthDialog = false;
            this.$router.push('/');
          }, 2000);
        })
        .catch((error) => {
          this.statusHeader = "Log In Unsuccessful";
          this.statusDescription = "Wrong Username/Password. Try Again!";
          this.statusSuccess = false;
          this.showAuthDialog = true;
        });
    },
    handleSignUp() {
      createUserWithEmailAndPassword(auth, this.email, this.password)
        .then((userCredential) => {
          const user = userCredential.user;
          updateProfile(user, {
            displayName: this.userName
          });

          // Store user data in Firestore
          setDoc(doc(db, "users", user.uid), {
            userName: this.userName,
            companyName: this.companyName, // Store company's name in the database
            userType: this.isSupplier ? "supplier" : "restaurant",
            points: this.isSupplier ? null : 0,
          })
            .then(() => {
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
            });
        })
        .catch((error) => {
          console.error("Error in Signing Up, Please Try Again!", error);
          this.statusHeader = "Signed Up Unsuccessful";
          this.statusDescription = "Error in Signing Up, Please Try Again!";
          this.statusSuccess = false;
          this.showAuthDialog = true;
        });
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
</style>