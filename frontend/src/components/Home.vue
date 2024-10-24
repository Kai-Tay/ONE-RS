<script setup>
import Navbar from './Navbar.vue';
import { Button } from './ui/button';
</script>

<template>
    <!-- <div class="container">
        Search
        <div class="my-5">
            <h1>Find Suppliers 🔍</h1>
            <div class="search-container">
                <input type="text" v-model="searchQuery" @input="filterListings" class="search-box my-0"
                    :placeholder="searchPlaceholder" />
                <button @click="performSearch" class="btn btn-primary btn-lg search-btn mx-3">🔍</button>
            </div>
            <div class="form-check form-switch my-2 mx-2">
                <input class="form-check-input" type="checkbox" role="switch" v-model="isAiSearch">
                <label class="form-check-label fs-5" for="flexSwitchCheckDefault">Use AI Search {{ isAiSearch ?
                    'enabled' : 'disabled' }}</label>
            </div>
        </div>

        Listings
        <div class="row">
            <div class="col-md-4 mb-4" v-for="listing in filteredListings" :key="listing.id">
                <div class="card h-100">
                    <img :src="listing.image" class="card-img-top" alt="Listing Image" />
                    <div class="card-body">
                        <h5 class="card-title">{{ listing.title }}</h5>
                        <p class="card-text">{{ listing.description }}</p>
                        <p class="card-text"><strong>Price:</strong> {{ listing.price }}</p>
                    </div>
                    <div class="card-footer">
                        <a :href="`/listings/${listing.id}`" class="btn btn-primary">View Details</a>
                    </div>
                </div>
            </div>
        </div>
    </div> -->

    <header class="bg-gray-900 py-5 h-80 flex flex-col justify-center">
        <div class="px-5 row gx-5 justify-center">
            <div class="col-lg-6">
                <div class="text-center my-5 ">
                    <!-- Welcome Text -->
                    <div class="text-4xl font-bold">
                        <h1 class="display-5 fw-bolder text-white mb-2" v-if="isLoggedIn">Welcome, {{ userName }}</h1>
                        <h1 class="display-5 fw-bolder text-white mb-2" v-else>Welcome to ONE.RS</h1>
                    </div>
                    <!-- SUBHEADERR -->
                    <div class="text-gray-500 text-2xl">
                        <div v-if="isLoggedIn">
                            <p class="lead text-white-50 mb-4" v-if="userType == 'supplier'">Start setting up your listings!</p>
                            <p class="lead text-white-50 mb-4" v-else>Start finding your ingredients from suppliers!</p>
                        </div>
                        <p class="lead text-white-50 mb-4" v-else>The best place for restaurants and suppliers to
                            connect!
                        </p>
                    </div>

                    <!-- Buttons for navigation -->
                    <div>
                        <div class="justify-center flex flex-inline "  v-if="isLoggedIn">
                            <a class="mx-5" href="#features" v-if="userType == 'supplier'"><Button>Find Suppliers!</Button></a>
                            <a class="mx-5" href="#/find" v-else><Button>Find Suppliers!</Button></a>
                            <a class="mx-5" href="#!"><Button variant="secondary">Learn More</Button></a>
                        </div>
                        <div class="grid gap-3 d-sm-flex justify-center" v-else>
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
                        <i class="bi bi-list-columns text-primary"></i>
                        <h2 class="h4 fw-bolder">Listings</h2>
                        <p></p>
                        <a class="text-decoration-none" href="#!">
                            Move to Listings
                            <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                    <div class="col-lg-3 mb-5 mb-lg-0 text-center">
                        <i class="bi bi-database-check text-primary"></i>
                        <h2 class="h4 fw-bolder">Real-time Database</h2>
                        <p>Paragraph of text beneath the heading to explain the heading. We'll add onto it with another
                            sentence and probably just keep going until we run out of words.</p>
                        <a class="text-decoration-none" href="#!">
                            Move to Real-time Database
                            <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                    <div class="col-lg-3 text-center">
                        <i class="bi bi-gear-wide-connected text-primary"></i>
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

        <!-- Buyer -->
        <section class="py-5 border-bottom" id="features" v-else>
            <div class="container px-5 my-5">
                <div class="row justify-content-center gx-5">
                    <div class="col-lg-3 mb-5 mb-lg-0 text-center">
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
                        <i class="bi bi-credit-card text-primary"></i>
                        <h2 class="h4 fw-bolder">Credit Score</h2>
                        <p>As a buyer, you have a credit score to maintain. These will increase for every payment made
                            on time to the supplier. Check your score here!</p>
                        <a class="text-decoration-none" href="#!">
                            Move to Credit Score
                            <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                    <div class="col-lg-3 text-center">
                        <i class="bi bi-gear-wide-connected text-primary"></i>
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
                    <h4 class="fw-bolder">Listings</h4>
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
            userType: "restaurant",
        };
    },
    created() {
        // Initially set the filtered listings to all listings
        this.filteredListings = this.listings;
    },
    methods: {
    },
    computed: {
        // Computed property to dynamically set the placeholder
        searchPlaceholder() {
            return this.isAiSearch ? 'Tell me your dishes!' : 'Search...';
        }
    }
};
</script>

<style></style>