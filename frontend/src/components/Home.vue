<script setup>
import Navbar from './Navbar.vue';
import { auth, db } from '../firebase.js';
import { doc, getDoc } from "firebase/firestore";
</script>

<template>
    <Navbar />

    <header class="bg-dark py-5">
        <div class="container px-5">
            <div class="row gx-5 justify-content-center">
                <div class="col-lg-6">
                    <div class="text-center my-5">
                        <h1 class="display-5 fw-bolder text-white mb-2" v-if="isLoggedIn">Welcome, {{ userName }}</h1>
                        <h1 class="display-5 fw-bolder text-white mb-2" v-else>Welcome to ONE.RS</h1>
                        <div v-if="isLoggedIn">
                            <p class="lead text-white-50 mb-4" v-if="userType == 'supplier'">Start setting up your
                                listings!</p>
                            <p class="lead text-white-50 mb-4" v-else>Start finding your ingredients from
                                suppliers!
                            </p>
                        </div>
                        <p class="lead text-white-50 mb-4" v-else>The best place for restaurants and suppliers to
                            connect!</p>
                        <div class="d-grid gap-3 d-sm-flex justify-content-sm-center" v-if="isLoggedIn">
                            <a class="btn btn-primary btn-lg px-4 me-sm-3" href="#features" v-if="isSupplier">Start
                                Listing</a>
                            <a class="btn btn-primary btn-lg px-4 me-sm-3" href="#features" v-else>Find
                                Suppliers</a>
                            <a class="btn btn-outline-light btn-lg px-4" href="#!">Learn More</a>
                        </div>
                        <div class="d-grid gap-3 d-sm-flex justify-content-sm-center" v-else>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- When Logged In -->
    <div v-if="isLoggedIn">
        <!-- Supplier -->
        <section class="py-5 border-bottom" id="features" v-if="userType == 'supplier'">
            <div class="container px-5 my-5">
                <div class="row justify-content-center gx-5">
                    <div class="col-lg-3 mb-5 mb-lg-0 text-center">
                        <i class="bi bi-list-columns text-primary fs-1"></i>
                        <h2 class="h4 fw-bolder">Manage Listings</h2>
                        <p></p>
                        <a class="text-decoration-none" href="#!">
                            Move to Listings
                            <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                    <div class="col-lg-3 mb-5 mb-lg-0 text-center">
                        <i class="bi bi-database-check text-primary fs-1"></i>
                        <h2 class="h4 fw-bolder">Real-time Database</h2>
                        <p></p>
                        <a class="text-decoration-none" href="#!">
                            Move to Real-time Database
                            <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                    <div class="col-lg-3 text-center">
                        <i class="bi bi-gear-wide-connected text-primary fs-1"></i>
                        <h2 class="h4 fw-bolder">Order Optimisation</h2>
                        <p></p>
                        <a class="text-decoration-none" href="#!">
                            Move to Order Optimisation
                            <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- Restaurant -->
        <section class="py-5 border-bottom" id="features" v-else>
            <div class="container px-5 my-5">
                <div class="row justify-content-center gx-5">
                    <div class="col-lg-3 mb-5 mb-lg-0 text-center fs-1">
                        <i class="bi bi-robot text-primary"></i>
                        <h2 class="h4 fw-bolder">AI Sourcing</h2>
                        <p>Find the ingredients needed for your restaurant using our AI Sourcing!
                            All you need to do is to input your ingredients and let the AI do the rest.</p>
                        <a class="text-decoration-none" href="#!">
                            Move to AI Sourcing
                            <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                    <div class="col-lg-3 mb-5 mb-lg-0 text-center">
                        <i class="bi bi-credit-card text-primary fs-1"></i>
                        <h2 class="h4 fw-bolder">Credit Score</h2>
                        <p>As a buyer, you have a credit score to maintain. These will increase for every payment made
                            on time to the supplier. Check your score here!</p>
                        <a class="text-decoration-none" href="#!">
                            Move to Credit Score
                            <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                    <div class="col-lg-3 text-center">
                        <i class="bi bi-gear-wide-connected text-primary fs-1"></i>
                        <h2 class="h4 fw-bolder">Order Optimisation</h2>
                        <p>Are you overbuying ingredients for your business? Use our order optimiser to analyse your
                            order history and plan out your next purchase!</p>
                        <a class="text-decoration-none" href="#!">
                            Move to Order Optimisation
                            <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- When Not Logged In -->
    <section class="py-5 border-bottom" v-else>
        <div class="container px-5 my-3">
            <div class="text-center mb-5">
                <h2 class="fw-bolder">Our Services</h2>
                <p class="lead mb-0">Find out what our website can do for you</p>
            </div>
            <div class="row justify-content-center mb-5">
                <div class="col-lg-6">
                    <h4 class="fw-bolder">AI Sourcing for Buyers</h4>
                    <p class="lead mb-0">Leverage the power of AI to source the finest ingredients with precision and
                        efficiency. Our advanced algorithms analyze quality, sustainability, and supplier data to ensure
                        that every ingredient meets your standards, streamlining the sourcing process for optimal
                        results.</p>
                </div>
                <div class="col-lg-3">
                    <!-- Picture Placeholder -->
                    <i class="bi bi-robot text-primary fs-1"></i>
                </div>
            </div>
            <div class="row justify-content-center mb-5">
                <div class="col-lg-3">
                    <!-- Picture Placeholder -->
                    <i class="bi bi-robot text-primary fs-1"></i>
                </div>
                <div class="col-lg-6">
                    <h4 class="fw-bolder">Real-time Database for Suppliers</h4>
                    <p class="lead mb-0">Monitor and manage supplier data with ease using our real-time dashboard.
                        Access up-to-date information on inventory, performance metrics, and compliance, all in one
                        intuitive interface. Make data-driven decisions instantly to keep your supply chain running
                        smoothly.</p>
                </div>
            </div>
            <div class="row justify-content-center mb-5">
                <div class="col-lg-6">
                    <h4 class="fw-bolder">Manage your Listings</h4>
                    <p class="lead mb-0">Leverage the power of AI to source the finest ingredients with precision and
                        efficiency. Our advanced algorithms analyze quality, sustainability, and supplier data to ensure
                        that every ingredient meets your standards, streamlining the sourcing process for optimal
                        results.</p>
                </div>
                <div class="col-lg-3">
                    <!-- Picture Placeholder -->
                    <i class="bi bi-robot text-primary fs-1"></i>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: 'Home',
    components: {
        Navbar,
    },
    data() {
        return {
            isLoggedIn: false,
            userName: "",
            userType: "",
        };
    },
    methods: {
        checkAuthentication() {
            onAuthStateChanged(auth, (user) => {
                if (user) {
                    // User is signed in, see docs for a list of available properties
                    const uid = user.uid;
                    this.isLoggedIn = true;

                    // Enter database and find userType
                    const docRef = doc(db, "users", uid);
                    getDoc(docRef).then((docSnap) => {
                        if (docSnap.exists()) {
                            this.userName = docSnap.data().userName;
                            this.userType = docSnap.data().userType;
                        }
                    });
                } else {
                    // User is signed out
                    this.isLoggedIn = false;
                }
            });
        }
    },
    mounted() {
        this.checkAuthentication();
    }
};
</script>