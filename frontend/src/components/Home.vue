<script setup>
import Navbar from './Navbar.vue';
import { Button } from './ui/button';
import { animate, spring, scroll, inView } from "motion";
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateTo = (route) => {
    router.push(route);
};
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

    <header class="bg-gray-900 py-5 h-screen flex flex-col justify-center">
        <div class="px-5 row gx-5 justify-center">
            <div class="col-lg-6">
                <div class="text-center my-5 ">
                    <!-- Welcome Text -->
                    <div class="text-4xl font-bold" ref="titleContainer">
                        <h1 class="display-5 fw-bolder text-white mb-2 " v-if="isLoggedIn">Welcome, {{ userName }}</h1>
                        <h1 class="display-5 fw-bolder text-white mb-2 opacity-0" v-else ref="mainTitle">Welcome to
                            ONE.RS</h1>
                    </div>
                    <!-- SUBHEADERR -->
                    <div class="text-gray-500 text-2xl">
                        <div v-if="isLoggedIn">
                            <p class="lead text-white-50 mb-4" v-if="userType == 'supplier'">Start setting up your
                                listings!</p>
                            <p class="lead text-white-50 mb-4" v-else>Start finding your ingredients from suppliers!</p>
                        </div>
                        <p class="lead text-white-50 mb-4" v-else>The best place for restaurants and suppliers to
                            connect!
                        </p>
                    </div>

                    <!-- Buttons for navigation -->
                    <div>
                        <div class="justify-center flex flex-inline " v-if="isLoggedIn && userType === 'supplier'">
                            <!-- <a class="mx-5" href="#features" v-if="userType == 'supplier'"><Button>Find
                                    Suppliers!</Button></a>
                            <a class="mx-5" href="#/find" v-else><Button>Find Suppliers!</Button></a>
                            <a class="mx-5" href="#!"><Button variant="secondary">Learn More</Button></a> -->
                            <Button class="mx-5" @click="scrollToFeatures" ref="learnMoreButton">Learn More</Button>
                        </div>
                        <div class="grid gap-3 d-sm-flex justify-center" v-else>
                            <Button class="mx-5" @click="scrollToFeatures" ref="learnMoreButton">Learn More</Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- When Logged In -->
    <div v-if="isLoggedIn">
        <!-- Supplier -->
        <section class="" id="features" v-if="userType == 'supplier'">
            <div class="grid grid-cols-3 h-screen" ref="featureGrid">
                <div class="bg-black text-white px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                    @click="navigateTo('/supplierInventory')" ref="listingsCard">
                    <div>
                        <i class="bi bi-camera text-primary text-3xl"></i>
                        <h2 class="text-3xl font-bold mt-4">Listings</h2>
                    </div>
                    <div class="mt-auto">
                        <p class="text-gray-400">Creating a listing is a breeze! Just snap a photo, write a quick
                            description, and set your price.</p>
                    </div>
                </div>

                <div class="bg-white px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                    @click="navigateTo('/supplierInventory')" ref="ordersCard">
                    <div>
                        <i class="bi bi-credit-card text-primary text-3xl"></i>
                        <h2 class="text-3xl font-bold mt-4">Receive Orders</h2>
                    </div>
                    <div class="mt-auto">
                        <p class="text-gray-600">As a supplier, you receive orders from buyers all over the world. You
                            can accept or reject the order.</p>
                    </div>
                </div>

                <div class="bg-gray-100 px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                    ref="checkoutCard">
                    <div>
                        <i class="bi bi-gear-wide-connected text-primary text-3xl"></i>
                        <h2 class="text-3xl font-bold mt-4">Checkout</h2>
                    </div>
                    <div class="mt-auto">
                        <p class="text-gray-600">We use Stripe to handle payments. You can set your payment preferences
                            in your account settings.</p>
                    </div>
                </div>
            </div>

            <div class="h-screen grid grid-rows-2 gap-4" ref="bottomGrid">
                <div class="bg-gray-100 px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                    ref="inventoryCard">
                    <div class="firstFade">
                        <i class="bi bi-gear-wide-connected text-primary text-3xl"></i>
                        <h2 class="hide text-3xl font-bold mt-4">Inventory Management</h2>
                    </div>
                    <div class="secondFade mt-auto">
                        <p class="hide text-gray-600">Monitor your inventory levels in real-time. Get insights into your
                            best-selling items and manage stock efficiently.</p>
                    </div>
                </div>

                <div class="bg-black text-white px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                    ref="paymentsCard">
                    <div class="firstFade">
                        <i class="bi bi-receipt text-primary text-3xl"></i>
                        <h2 class="hide text-3xl font-bold mt-4">Automated Payments</h2>
                    </div>
                    <div class="secondFade mt-auto">
                        <p class="hide mb-5">View and manage all your orders in one place. Track deliveries and maintain your
                            reputation.</p>
                    </div>
                </div>
            </div>
        </section>


        <!-- Restaurant -->
        <section id="features" v-else>
            <div class="grid grid-cols-3 h-screen">
                <!-- Map Image of Restaurants Connecting -->
                <div class="flex flex-col justify-between bg-black text-white px-5" @click="navigateTo('/find')"
                    ref="findCard">
                    <h2 class="fw-bolder text-3xl mt-3">Find Suppliers</h2>
                    <div class="mb-5">
                        <p class="mb-5">Find the ingredients needed for your restaurant using our AI Sourcing!
                            All you need to do is to input your ingredients and let the AI do the rest.</p>
                    </div>
                </div>

                <div class="flex flex-col justify-between px-5" ref="orderCard">
                    <h2 class="fw-bolder text-3xl mt-3">Place Order</h2>
                    <div class="mb-5">
                        <p class="mb-5">As a buyer, you have a credit score to maintain. These will increase for every
                            payment
                            made
                            on time to the supplier. Check your score here!</p>
                    </div>
                </div>

                <div class="flex flex-col justify-between px-5" ref="paymentCard">
                    <h2 class="fw-bolder text-3xl mt-3">Checkout</h2>
                    <div class="mb-5">
                        <p class="mb-5">Are you overbuying ingredients for your business? Use our order optimiser to
                            analyse your
                            order history and plan out your next purchase!</p>
                    </div>
                </div>
            </div>

            <div class="h-screen grid grid-rows-2 gap-4" ref="bottomGrid">
                <div class="bg-gray-100 px-8 py-12 flex flex-col cursor-pointer" ref="aiCard">
                    <div class="firstFade">
                        <h2 class="hide text-3xl font-bold mt-4">AI Sourcing</h2>
                    </div>
                    <div class="secondFade mt-auto">
                        <p class="hide text-gray-600">Find the ingredients needed for your restaurant using our AI
                            Sourcing!
                            All you need to do is to input your ingredients and let the AI do the rest.</p>
                    </div>
                </div>

                <div class="bg-black text-white px-8 py-12 flex flex-col cursor-pointer" ref="dashboardCard">
                    <div class="firstFade">
                        <h2 class="hide text-3xl font-bold mt-4">Automated Payments</h2>
                    </div>
                    <div class="secondFade mt-auto">
                        <p class="hide mb-5">View and manage all your orders in one place. Track deliveries and maintain
                            your
                            reputation.</p>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- When Not Logged In -->
    <section class="border-bottom" id="features" v-else>
        <div class="grid grid-cols-3 h-screen">
            <!-- AI Sourcing Card -->
            <div
                class="bg-black text-white px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90">
                <div>
                    <i class="bi bi-robot text-primary text-3xl"></i>
                    <h2 class="text-3xl font-bold mt-4">AI Sourcing for Buyers</h2>
                </div>
                <div class="mt-auto">
                    <p class="text-gray-400">Leverage the power of AI to source the finest ingredients with precision
                        and efficiency. Our advanced algorithms analyze quality, sustainability, and supplier data to
                        ensure that every ingredient meets your standards.</p>
                </div>
                <div class="col-lg-3">
                    <!-- Picture Placeholder -->
                    <i class="bi bi-robot text-primary fs-1"></i>
                </div>
            </div>

            <!-- Real-time Database Card -->
            <div class="bg-white px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90">
                <div>
                    <i class="bi bi-gear-wide-connected text-primary text-3xl"></i>
                    <h2 class="text-3xl font-bold mt-4">Real-time Database for Suppliers</h2>
                </div>
                <div class="mt-auto">
                    <p class="text-gray-600">Monitor and manage supplier data with ease using our real-time dashboard.
                        Access up-to-date information on inventory, performance metrics, and compliance, all in one
                        intuitive interface.</p>
                </div>
                <div class="col-lg-3">
                    <i class="bi bi-robot text-primary fs-1"></i>
                    <!-- Picture Placeholder -->
                </div>
            </div>

            <div class="bg-gray-100 px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                @click="navigateTo('/login')">
                <div>
                    <i class="bi bi-camera text-primary text-3xl"></i>
                    <h2 class="text-3xl font-bold mt-4">Sign Up</h2>
                </div>
                <div class="mt-auto">
                    <p class="text-gray-600">Ready to transform your F&B business? Join one-rs today and tap into our
                        growing network of trusted suppliers and innovative restaurants. Experience seamless ordering,
                        real-time inventory updates, and AI-powered sourcing that saves you time and money. Whether
                        you're a supplier looking to expand your reach or a restaurant seeking quality ingredients,
                        one-rs connects you to opportunities that matter. Don't miss out on the digital revolution in
                        F&B sourcing – sign up now and be part of a community that's reshaping the industry.</p>
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
    created() {
        // Initially set the filtered listings to all listings
        this.filteredListings = this.listings;
    },
    methods: {
        scrollToFeatures() {
            const features = document.querySelector("#features");

            if (features) {
                features.scrollIntoView({ behavior: 'smooth' });

                if (this.$refs.learnMoreButton) {
                    animate(this.$refs.learnMoreButton, {
                        scale: [1, 0.95, 1],
                        opacity: [1, 0.7, 1]
                    }, {
                        duration: 0.3
                    });
                }
            }
        }
    },
    computed: {
        // Computed property to dynamically set the placeholder
        searchPlaceholder() {
            return this.isAiSearch ? 'Tell me your dishes!' : 'Search...';
        }
    },
    mounted() {
        // Set login state first before any animations
        this.userName = sessionStorage.userName;
        this.userType = sessionStorage.userType;
        this.isLoggedIn = this.userName != null;  // Set this immediately

        this.$nextTick(() => {
            // Title animation
            const titleElement = document.querySelector('.display-5');
            if (titleElement) {
                animate(titleElement, {
                    opacity: [0, 1],
                    y: [50, 0]
                }, {
                    duration: 1,
                    easing: spring({ stiffness: 50, damping: 15 })
                });
            }

            // Only run for supplier
            if (this.userType === 'supplier') {
                const cards = ['listingsCard', 'ordersCard', 'checkoutCard', 'inventoryCard', 'paymentsCard'];

                cards.forEach((card, index) => {
                    const element = this.$refs[card];
                    if (element) {
                        scroll(
                            animate(element, {
                                y: [50, 0]
                            }, {
                                delay: index * 0.15,
                                duration: 0.8
                            }),
                            {
                                target: element,
                                offset: ["start end", "end start"]
                            }
                        );
                    }
                });
            }

            // Animation for Bottom Grid
            const first = document.querySelectorAll('.firstFade');
            const second = document.querySelectorAll('.secondFade');
            if (first) {
                inView(first, ({ target }) => {
                    animate(
                        target.querySelector("h2"),
                        {
                            opacity: 1,
                            transform: "none"
                        },
                        {
                            delay: 0.2,
                            duration: 0.9,
                            easing: [0.17, 0.55, 0.55, 1]
                        }
                    );
                });
            }

            if (second) {
                inView(second, ({ target }) => {
                    animate(
                        target.querySelector("p"),
                        {
                            opacity: 1,
                            transform: "none"
                        },
                        {
                            delay: 0.2,
                            duration: 0.9,
                            easing: [0.17, 0.55, 0.55, 1]
                        }
                    );
                });
            }
        });
    },
};
</script>

<style>
.hide {
    transform: translateX(-100px);
    opacity: 0;
}
</style>