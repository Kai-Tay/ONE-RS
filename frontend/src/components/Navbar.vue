<script setup>
import { onAuthStateChanged, signOut } from "firebase/auth";
import {auth} from '../firebase.js';
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand " href="#">🧑‍🍳 ONE.RS</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText"
                aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarText">
                <!-- Restaurant Tabs -->
                <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="userType == 'restaurant'">
                    <li class="nav-item">
                        <a class="nav-link" :class="{ active: $route.path === '/' }" aria-current="page" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :class="{ active: $route.path === '/buyer' }" href="#/find">Find</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :class="{ active: $route.path === '/?' }" href="#/">Orders</a>
                    </li>
                </ul>

                <!-- Supplier Tabs -->
                <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-else>
                    <li class="nav-item">
                        <a class="nav-link" :class="{ active: $route.path === '/' }" aria-current="page" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :class="{ active: $route.path === '/find' }" href="#/find">Create Listing</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :class="{ active: $route.path === '/?' }" href="#/supplier">Order Statistics</a>
                    </li>
                </ul>

                <span class="navbar-text" v-if="!isLoggedIn">
                    <button type="button" class="btn btn-success"
                        @click="handleLogin">Login / Sign Up</button>
                </span>
                <span class="navbar-text" v-else>
                    <div class="d-inline" style="margin-right: 10px;">{{ userName }}</div>
                    <button type="button" class="btn btn-outline-danger" @click="handleLogOut">Logout</button>
                </span>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'Navbar',
    data() {
        return {
            isLoggedIn: false,
            userName: "",
            userType: "restaurant",
        };
    },
    methods: {
        // Check if user is already logged in and change the nav bar accordingly
        checkAuthentication() {
            onAuthStateChanged(auth, (user) => {
                if (user) {
                    // User is signed in, see docs for a list of available properties
                    const uid = user.uid;
                    this.userName = user.displayName;
                    this.isLoggedIn = true;
                    console.log(uid)
                } else {
                    // User is signed out
                    this.isLoggedIn = false;
                    this.userType = "restaurant";
                }
            });

        },
        handleLogin() {
            this.$router.push('/login');
        },
        handleLogOut() {
            signOut(auth).then(() => {
                alert("User logged out successfully!");
                // Redirect the user to the login page or handle it appropriately
            }).catch((error) => {
                alert("Error logging out: ", error);
            });
        },
    },
    mounted() {
        this.checkAuthentication();
    }
};
</script>

<style>
.navbar{
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.navbar-brand {
  font-size: 25px;
}
</style>