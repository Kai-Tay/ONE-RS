<script setup>
import Navbar from './Navbar.vue';
import auth from '../firebase.js';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile } from "firebase/auth";
</script>

<!-- HTML STUFF -->
<template>
    <Navbar />
    <div class="login-container">
        <form @submit.prevent="handleLogin" v-if="isLogin">
            <h1>Login</h1>
            <div class="form-group">
                <label for="email">Email </label>
                <input type="email" id="email" v-model="email" placeholder="Enter your email" required />
            </div>

            <div class="form-group">
                <label for="password">Password </label>
                <input type="password" id="password" v-model="password" placeholder="Enter your password" required />
            </div>
            <button type="submit">Log In</button>
        </form>

        <form @submit.prevent="handleSignUp" v-else>
            <h1>Sign Up</h1>
            <div class="form-group">
                <label for="email">Name </label>
                <input type="text" v-model="userName" placeholder="Enter Your username" required />
            </div>

            <div class="form-group">
                <label for="email">Email </label>
                <input type="email" id="email" v-model="email" placeholder="Enter your email" required />
            </div>

            <div class="form-group">
                <label for="password">Password </label>
                <input type="password" id="password" v-model="password" placeholder="Enter your password" required />
            </div>
            <button type="submit">Sign Up</button>
        </form>

        <button class="d-inline" @click="toggleLogin">{{ switchLabel }}</button>
    </div>
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
            isLogin: true,
            switchLabel: 'Sign Up Instead',
        };
    },
    methods: {
        toggleLogin() {
            this.isLogin = !this.isLogin;
            if (this.isLogin) {
                this.switchLabel = "Sign Up Instead"
            } else {
                this.switchLabel = "Login Instead"
            }

        },
        handleLogin() {
            signInWithEmailAndPassword(auth, this.email, this.password)
                .then((userCredential) => {
                    alert("Signed In")
                    // Signed in -> Redirect to home page
                    const user = userCredential.user;
                    console.log(userCredential)
                    this.$router.push('/');
                })
                .catch((error) => {
                    // Wrong password
                    alert("Wrong Username/Password. Try Again!")
                    const errorCode = error.code;
                    const errorMessage = error.message;
                });
        },
        handleSignUp() {
            createUserWithEmailAndPassword(auth, this.email, this.password)
                .then((userCredential) => {
                    // Signed up + Store UserName
                    const user = userCredential.user;
                    updateProfile(user, {
                        displayName: this.userName 
                    })
                    alert("User signed up")
                })
                .catch((error) => {
                    alert("Error in Signing Up, Please Try Again!")
                    const errorCode = error.code;
                    const errorMessage = error.message;
                    // ..
                });
        }
    }
};
</script>

<!-- CSS STUFF -->
<style>
.login-container {
    background-color: whitesmoke;
    color: black;
}
</style>