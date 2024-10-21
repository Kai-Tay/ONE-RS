<script setup>
import { onAuthStateChanged, signOut } from "firebase/auth";
import { auth, db } from '../firebase.js';
import { doc, getDoc } from "firebase/firestore";
import { Button } from "./ui/button/index.js";
</script>

<template>
    <nav class="h-16 flex flex-inline items-center justify-between">
        <!-- Logo + Nav Bar-->
        <div class="mx-5 text-xl flex flex-inline">
            <div>🧑‍🍳 ONE.RS</div>
            <div :class="{ 'hidden lg:flex': !isMenuOpen }"
                class="flex flex-col lg:flex-row lg:items-center w-full lg:w-auto text-sm mx-5">
                <!-- Restaurant Tabs -->
                <ul class="flex flex-col lg:flex-row mb-4 lg:mb-0 space-x-4" v-if="userType == 'restaurant'">
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/' }" href="#">Home</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/find' }" href="#/find">Find
                            Suppliers</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/order-history' }"
                            href="#/order-history">Order History</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/order-analytics' }"
                            href="#/order-analytics">Order Analytics</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/buyerDashboard' }"
                            href="#/buyerDashboard">Dashboard</a></li>
                </ul>

                <!-- Supplier Tabs -->
                <ul class="flex flex-col lg:flex-row mb-4 lg:mb-0 space-x-4" v-else>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/' }" href="#">Home</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/current-orders' }"
                            href="#/supplier">Current Orders</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/inventory-management' }"
                            href="#/supplier">Inventory Management</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/supplierDashboard' }"
                            href="#/supplierDashboard">Dashboard</a></li>
                </ul>
            </div>

        </div>

        <!-- Login Button -->
        <div class="mx-5">
            <div v-if="!isLoggedIn" class=" flex justify-end ">
                <Button class="" @click="handleLogin" variant="green">Login / Sign Up</Button>
            </div>
            <div v-else class="flex items-center gap-4">
                <span>{{ userName }}</span>
                <Button class="" @click="handleLogOut" variant="destructive">Logout</Button>
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

                    user.getIdTokenResult().then((idTokenResult) => {
                        // Retrieve expirationTime from the token result
                        const expirationTime = new Date(idTokenResult.authTime).getTime() + 3600000; // Convert to milliseconds
                        const currentTime = new Date().getTime(); // Get current time in milliseconds

                        // Check if the token is expired
                        if (currentTime > expirationTime) {
                            signOut(auth).then(() => {
                                console.log("Session expired. User logged out.");

                                this.isLoggedIn = false;
                                this.userType = "restaurant";

                            }).catch((error) => {
                                alert("Error logging out: ", error);
                            });

                        } else {
                            // Enter database and find userType
                            const docRef = doc(db, "users", uid);
                            getDoc(docRef).then((docSnap) => {
                                if (docSnap.exists()) {
                                    this.userType = docSnap.data().userType;
                                }
                            });


                        }
                    });
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
                // Redirect the user to the login page or handle it appropriately
                this.$router.push('/');
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
.navbar {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
    font-size: 25px;
}
</style>