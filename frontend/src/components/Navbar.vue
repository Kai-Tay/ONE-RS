<script setup>
import { onAuthStateChanged, signOut } from "firebase/auth";
import { auth, db } from '../firebase.js';
import { doc, getDoc } from "firebase/firestore";
import { Button } from "./ui/button/index.js";
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import AuthenticationDialog from "./Authentication/AuthenticationDialog.vue";


</script>


<template>
    <div class="w-full">
        <!-- <nav class="h-16 flex items-center justify-between text-gray-900" :class="navbarClasses"> -->
        <nav class="h-16 flex items-center justify-between transition-colors duration-300" :class="[navbarClasses, $route.path === '/' ? 'absolute top-0 left-0 right-0 z-50' : 'relative']">
            <!-- Logo + Nav Bar-->
            <div class="mx-5 text-xl flex flex-inline">
                <div class="text-2xl font-bold ">ONE.RS 🧑‍🍳 </div>
                <div class="lg:flex flex-col lg:flex-row lg:items-center w-full lg:w-auto text-sm mx-5 hidden"
                    v-if="isLoggedIn == true">
                    <!-- Restaurant Tabs -->
                    <ul class="flex flex-col lg:flex-row mb-4 lg:mb-0 space-x-6" v-if="userType == 'restaurant'">
                        <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/' }" href="#">Home</a></li>
                        <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/find' }" href="#/find">Find
                                Suppliers</a></li>
                        <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/buyerOrders' }"
                                href="#/buyerOrders">Orders</a></li>
                        <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/buyerDashboard' }"
                                href="#/buyerDashboard">Dashboard</a></li>
                    </ul>

                    <!-- Supplier Tabs -->
                    <ul class="flex flex-col lg:flex-row mb-4 lg:mb-0 space-x-6" v-else>
                        <li><a class="nav-link" :class="{ 'font-extrabold': $route.path === '/' }" href="#">Home</a>
                        </li>
                        <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/supplierOrders' }"
                                href="#/supplierOrders">Orders</a></li>
                        <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/supplierInventory' }"
                                href="#/supplierInventory">Inventory Management</a></li>
                    </ul>
                </div>

                <div class="lg:flex flex-col lg:flex-row lg:items-center w-full lg:w-auto text-sm mx-5 hidden" v-else>
                    <!-- Not Logged In Tabs -->
                    <ul class="flex flex-col lg:flex-row mb-4 lg:mb-0 space-x-6">
                        <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/' }" href="#">Home</a></li>
                    </ul>
                </div>

            </div>

            <!-- Login Button -->
            <div class="mx-5 flex flex-inline">
                <!-- Hamburger Icon (Visible on small screens) -->
                <Button @click="isMenuOpen = !isMenuOpen" class="ml-4 lg:hidden" variant="secondary">
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
                    <div class="flex flex-inline items-center space-x-2" @click="handleProfileClick"
                        style="cursor: pointer">
                        <span>
                            <Avatar class="border-2 border-black">
                                <AvatarImage src="https://github.com/radix-vue.png" alt="@radix-vue" />
                                <AvatarFallback>{{ userName }}</AvatarFallback>
                            </Avatar>
                        </span>
                        <div>{{ userName }}</div>
                    </div>
                    <Button class="" @click="handleLogOut" variant="destructive">Logout</Button>
                </div>
            </div>

        </nav>
        <!-- Hamburger Version of Nav Bar -->
        <div :class="[{ 'hidden': !isMenuOpen, 'lg:hidden': true },{'mt-16': $route.path == '/'}, navbarClasses]" class="px-5 pb-5 space-y-4" v-if="isLoggedIn == true">
            <ul class="flex flex-col items-left space-y-4" v-if="userType == 'restaurant'">
                <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/' }" href="#">Home</a></li>
                <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/find' }" href="#/find">Find
                        Suppliers</a></li>
                <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/buyerOrders' }"
                        href="#/buyerOrders">Orders</a></li>
                <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/buyerDashboard' }"
                        href="#/buyerDashboard">Dashboard</a></li>
            </ul>
            <ul class="flex flex-col items-left space-y-4" v-else>
                <li><a class="nav-link" :class="{ 'font-extrabold': $route.path === '/' }" href="#">Home</a>
                </li>
                <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/supplierOrders' }"
                        href="#/supplierOrders">Orders</a></li>
                <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/supplierInventory' }"
                        href="#/supplierInventory">Inventory Management</a></li>
            </ul>
        </div>

        <div v-else class="lg:hidden flex items-center space-x-5">
            <div class="flex flex-inline items-center space-x-2" @click="handleProfileClick"
                style="cursor: pointer">
                <span>
                    <Avatar class="border-2 border-black">
                        <AvatarImage src="https://github.com/radix-vue.png" alt="@radix-vue" />
                        <AvatarFallback>{{ userName }}</AvatarFallback>
                    </Avatar>
                </span>
                <div>{{ userName }}</div>
            </div>
            <Button class="" @click="handleLogOut" variant="destructive">Logout</Button>
        </div>
            
            <div :class="[{ 'hidden': !isMenuOpen, 'lg:hidden': true },{'mt-16': $route.path == '/'}, navbarClasses]" class="px-5 pb-5 space-y-4" v-else>
            <ul class="flex flex-col items-left space-y-4">
                <li><a class="nav-link" :class="{ 'font-bold': $route.path === '/' }" href="#">Home</a></li>
            </ul>
            <div v-if="!isLoggedIn" class="lg:hidden items-center gap-4">
                <Button class="" @click="handleLogin" variant="green">Login / Sign Up</Button>
            </div>
        </div>
        
    </div>
    
    <!-- Sign Out Success Dialog -->
    <AuthenticationDialog :showDialog="showAuthDialog" :status="statusHeader" :description="statusDescription"
        :success="statusSuccess" @update:showDialog="showAuthDialog = $event" />


</template>

<script>
export default {
    name: 'Navbar',
    watch: {
        // Watching for route changes
        $route(to) {
            this.currentRoute = to.path;

            // Check if user is logged in
            this.checkSessionStorage();

            // Hide hamburger menu on route change
            this.isMenuOpen = false;
        }
    },
    data() {
        return {
            // Nav Bar Display
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
        checkSessionStorage() {
            if (sessionStorage.getItem('uid') != null) {
                console.log("User is logged in HEHEHARHAR");
                this.isLoggedIn = true;
                this.userName = sessionStorage.getItem('userName');
                this.userType = sessionStorage.getItem('userType');
            } else {
                console.log("User is not logged in HEHEHARHAR");
                this.isLoggedIn = false;
            }

        },
        checkAuthentication() {
            // Check if session storage has the user's data
            this.checkSessionStorage();

            onAuthStateChanged(auth, (user) => {
                if (user) {
                    // User is signed in
                    user.getIdTokenResult().then((idTokenResult) => {
                        // Retrieve expirationTime from the token result
                        const expirationTime = new Date(idTokenResult.authTime).getTime() + 3600000; // Convert to milliseconds
                        const currentTime = new Date().getTime(); // Get current time in milliseconds
                        const uid = idTokenResult.claims.user_id;
                        console.log("Current time: ", currentTime);
                        console.log("Auth Expiration time: ", expirationTime);
                        // Check if the token is expired
                        if (currentTime > expirationTime) {
                            signOut(auth).then(() => {
                                sessionStorage.clear();

                                // Redirect the user to the login page or handle it appropriately
                                this.statusHeader = "Session Timed Out";
                                this.statusDescription = "Please Login Again!";
                                this.showAuthDialog = true;

                                // Update vue variables
                                this.checkSessionStorage();

                                // Automatically close the dialog after 2 seconds
                                setTimeout(() => {
                                    this.showAuthDialog = false;
                                }, 2000);
                                this.$router.push('/');

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
                    // Clear cookies (Bug fix)
                    sessionStorage.clear();
                }
            });
        },
        handleLogin() {
            this.$router.push('/login');
        },
        handleProfileClick() {
            this.$router.push('/profile');
        },
        handleLogOut() {
            signOut(auth).then(() => {
                sessionStorage.clear();

                // Redirect the user to the login page or handle it appropriately
                this.statusHeader = "Logged Out";
                this.statusDescription = "See you again! Redirecting to the home page...";
                this.showAuthDialog = true;

                // Update vue variables
                this.checkSessionStorage();

                // Automatically close the dialog after 2 seconds
                setTimeout(() => {
                    this.showAuthDialog = false;
                }, 2000);
                this.$router.push('/');

            }).catch((error) => {
                alert("Error logging out: ", error);
            });
        },
    },
    mounted() {
        this.checkAuthentication();
    },
    computed: {
    navbarClasses() {
        return this.$route.path === '/' ? 'bg-gray-900 text-white' : 'bg-transparent text-gray-900';
    }
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