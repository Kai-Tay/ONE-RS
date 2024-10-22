<script setup>
import { onAuthStateChanged, signOut } from "firebase/auth";
import { auth, db } from '../firebase.js';
import { doc, getDoc } from "firebase/firestore";
import { Button } from "./ui/button/index.js";
import AuthenticationDialog from "./Authentication/AuthenticationDialog.vue";
</script>

<template>
    <div>
        <nav class="h-16 flex items-center justify-between shadow-lg">
            <!-- Logo + Nav Bar-->
            <div class="mx-5 text-xl flex flex-inline">
                <div>🧑‍🍳 ONE.RS</div>
                <div class="lg:flex flex-col lg:flex-row lg:items-center w-full lg:w-auto text-sm mx-5 hidden">
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
            <div class="mx-5 flex flex-inline">
                <!-- Hamburger Icon (Visible on small screens) -->
                <Button @click="isMenuOpen = !isMenuOpen" class="ml-4 lg:hidden">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                </Button>
                <div v-if="!isLoggedIn" class="lg:flex justify-end hidden">
                    <Button class="" @click="handleLogin" variant="green">Login / Sign Up</Button>
                </div>
                <div v-else class="lg:flex items-center gap-4 hidden">
                    <span>{{ userName }}</span>
                    <Button class="" @click="handleLogOut" variant="destructive">Logout</Button>
                </div>
            </div>

        </nav>
        <!-- Hamburger Version of Nav Bar -->
        <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
            <div :class="{ 'hidden': isMenuOpen, 'lg:hidden': true }">
                <ul class="flex flex-col items-left space-y-4 pb-5 px-5">
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/' }" href="#">Home</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/find' }" href="#/find">Find
                            Suppliers</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/order-history' }"
                            href="#/order-history">Order History</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/order-analytics' }"
                            href="#/order-analytics">Order Analytics</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/buyerDashboard' }"
                            href="#/buyerDashboard">Dashboard</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/current-orders' }"
                            href="#/supplier">Current Orders</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/inventory-management' }"
                            href="#/supplier">Inventory Management</a></li>
                    <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/supplierDashboard' }"
                            href="#/supplierDashboard">Dashboard</a></li>
                </ul>
            </div>
        </transition>
    </div>
    <!-- Sign Out Success Dialog -->
    <AuthenticationDialog :showDialog="showAuthDialog" :status="statusHeader" :description="statusDescription"
        :success="statusSuccess" @update:showDialog="showAuthDialog = $event" />


</template>

<script>
export default {
    name: 'Navbar',
    data() {
        return {
            isMenuOpen: false,
            isLoggedIn: false,
            userName: "",
            userType: "restaurant",


            // Dialog
            showAuthDialog: false,
            statusHeader: "",
            statusDescription: "",
            statusSuccess: true,
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
                                this.updateParentLoggedOut();

                            }).catch((error) => {
                                alert("Error logging out: ", error);
                            });

                        } else {
                            // Enter database and find userType
                            const docRef = doc(db, "users", uid);
                            getDoc(docRef).then((docSnap) => {
                                if (docSnap.exists()) {
                                    this.userType = docSnap.data().userType;
                                    this.updateParentLogIn();
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

                this.updateParentLoggedOut();
                // Automatically close the dialog after 2 seconds
                this.statusHeader = "Logged Out Successfully";
                this.statusDescription = "See you again! Redirecting to the home page...";
                this.showAuthDialog = true;
                // setTimeout(() => {
                //     this.showAuthDialog = false;
                // }, 2000);
                this.$router.push('/');

            }).catch((error) => {
                alert("Error logging out: ", error);
            });
        },
        updateParentLogIn() {
            this.$emit('userName', this.userName);
            this.$emit('userType', this.userType);
            this.$emit('isLoggedIn', this.isLoggedIn);
            this.$emit('uid', uid);
        },
        updateParentLoggedOut() {
            this.$emit('userName', "");
            this.$emit('userType', "restaurant");
            this.$emit('isLoggedIn', false);
            this.$emit('uid', "");
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