<script setup>
import Navbar from './Navbar.vue';
// import { Button } from './ui/button';
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
    <div class="min-h-screen flex flex-col">
        <!-- Navbar integrated directly in home page -->
        <Navbar v-if="$route.path === '/'" class="absolute top-0 left-0 right-0 z-50" />


        <header class="bg-gray-900 h-screen flex flex-col p-8" @click="scrollToFeatures">
            <!-- Logo Section (Top Left) -->
            <!-- <div class="flex-none">
                <h2 class="text-white text-2xl font-bold">ONE.RS 🧑‍🍳</h2>
            </div> -->

            <!-- Main Welcome Text (Center Left) -->
            <div class="flex-grow flex items-center">
                <div class="max-w-2xl">
                    <div class="text-7xl font-bold" ref="titleContainer">
                        <h1 class="text-left text-white mb-2" v-if="isLoggedIn">
                            Welcome, {{ userName }}
                        </h1>
                        <h1 class="text-left text-white mb-2" v-else ref="mainTitle">
                            Welcome to
                            <br />
                            ONE.RS
                        </h1>
                    </div>
                </div>
            </div>

            <!-- Subheader (Bottom Left) -->
            <div class="flex-none max-w-2xl">
                <div class="text-gray-200 text-2xl">
                    <div v-if="isLoggedIn">
                        <p class="text-left text-gray-400" v-if="userType == 'supplier'">
                            Start setting up your listings!
                        </p>
                        <p class="text-left text-gray-400" v-else>
                            Start finding your ingredients from suppliers!
                        </p>
                    </div>
                    <p class="text-left text-gray-400" v-else>
                        The best place for restaurants and
                        <br />
                        suppliers to connect!
                    </p>
                </div>
            </div>

            <!-- Right Side Image (INSERT IMAGE) -->
            <div class="w-1/2 flex items-center justify-center">
                <img src="" alt="" class="max-h-full object-cover rounded-lg" />
            </div>
        </header>

        <!-- When Logged In -->
        <div v-if="isLoggedIn">
            <!-- Supplier -->
            <section class="" id="features" v-if="userType == 'supplier'">
                <div class="grid grid-cols-1 md:grid-cols-3 h-screen" ref="featureGrid">
                    <div class="bg-black text-white px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                        @click="navigateTo('/supplierInventory')" ref="listingsCard" @mouseover="hoverAnimate($event)"
                        @mouseout="hoverOffAnimate($event)">
                        <div>
                            <i class="bi bi-camera text-primary text-3xl"></i>
                            <h2 class="text-4xl font-bold mt-4">Step 1:
                                <br>Listings
                            </h2>
                        </div>
                        <div class="mt-auto">
                            <p class="text-gray-400">Creating a listing is a breeze! Just snap a photo, write a quick
                                description, and set your price.</p>
                        </div>
                    </div>

                    <div class="bg-white px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                        @click="navigateTo('/supplierInventory')" ref="ordersCard" @mouseover="hoverAnimate($event)"
                        @mouseout="hoverOffAnimate($event)">
                        <div>
                            <h2 class="text-4xl font-bold mt-4">Step 2:
                                <br>Receive Orders
                            </h2>
                        </div>
                        <div class="mt-auto">
                            <p class="hide text-gray-600">As a supplier, you receive orders from buyers all over the world.
                                You
                                can accept or reject the order.</p>
                        </div>
                    </div>

                    <div class="bg-gray-100 px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                        ref="checkoutCard" @mouseover="hoverAnimate($event)" @mouseout="hoverOffAnimate($event)">
                        <div>
                            <h2 class="text-4xl font-bold mt-4">Step 3:
                                <br>Checkout
                            </h2>
                        </div>
                        <div class="mt-auto">
                            <p class="hide text-gray-600">We use Stripe to handle payments. You can set your payment
                                preferences
                                in your account settings.</p>
                        </div>
                    </div>
                </div>

                <div class="h-screen grid grid-rows-2 gap-4" ref="bottomGrid">
                    <div class="bg-gray-100 px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                        ref="inventoryCard">
                        <div class="firstFade">
                            <i class="bi bi-gear-wide-connected text-primary text-3xl"></i>
                            <h2 class="hide text-4xl font-bold mt-4">Inventory Management</h2>
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
                            <h2 class="hide text-4xl font-bold mt-4">Automated Payments</h2>
                        </div>
                        <div class="secondFade mt-auto">
                            <p class="hide mb-5">View and manage all your orders in one place. Track deliveries and maintain
                                your
                                reputation.</p>
                        </div>
                    </div>
                </div>
            </section>


            <!-- Restaurant -->
            <section id="features" v-else>
                <div class="grid grid-cols-1 md:grid-cols-3 h-screen">
                    <!-- Map Image of Restaurants Connecting -->
                    <div class="flex flex-col justify-between bg-black text-white px-5" @click="navigateTo('/find')"
                        ref="findCard" @mouseover="hoverAnimate($event)" @mouseout="hoverOffAnimate($event)">
                        <h2 class="text-4xl font-bold mt-4">Step 1:
                            <br>Find Suppliers
                        </h2>
                        <div class="mb-5">
                            <p class="mb-5">Find the ingredients needed for your restaurant using our AI Sourcing!
                                All you need to do is to input your ingredients and let the AI do the rest.</p>
                        </div>
                    </div>

                    <div class="flex flex-col justify-between px-5" ref="orderCard" @mouseover="hoverAnimate($event)"
                        @mouseout="hoverOffAnimate($event)">
                        <h2 class="text-4xl font-bold mt-4">Step 2:
                            <br>Place Order
                        </h2>
                        <div class="mb-5">
                            <p class="hide mb-5">As a buyer, you have a credit score to maintain. These will increase for
                                every
                                payment
                                made
                                on time to the supplier. Check your score here!</p>
                        </div>
                    </div>

                    <div class="flex flex-col justify-between px-5" ref="paymentCard" @mouseover="hoverAnimate($event)"
                        @mouseout="hoverOffAnimate($event)">
                        <h2 class="text-4xl font-bold mt-4">Step 3:
                            <br>Checkout
                        </h2>
                        <div class="mb-5">
                            <p class="hide mb-5">Are you overbuying ingredients for your business? Use our order optimiser
                                to
                                analyse your
                                order history and plan out your next purchase!</p>
                        </div>
                    </div>
                </div>

                <div class="h-screen grid grid-rows-3 gap-4" ref="bottomGrid">
                    <div class="bg-gray-100 px-8 py-12 flex flex-col cursor-pointer" ref="aiCard">
                        <div class="firstFade">
                            <h2 class="hide text-4xl font-bold mt-4">AI Sourcing</h2>
                        </div>
                        <div class="secondFade mt-auto">
                            <p class="hide text-gray-600">Find the ingredients needed for your restaurant using our AI
                                Sourcing!
                                All you need to do is to input your ingredients and let the AI do the rest.</p>
                        </div>
                    </div>

                    <div class="bg-black text-white px-8 py-12 flex flex-col cursor-pointer" ref="paymentsCard">
                        <div class="firstFade">
                            <h2 class="hide text-4xl font-bold mt-4">Automated Payments</h2>
                        </div>
                        <div class="secondFade mt-auto">
                            <p class="hide mb-5">View and manage all your orders in one place. Track deliveries and maintain
                                your
                                reputation.</p>
                        </div>
                    </div>

                    <div class="bg-gray-100 px-8 py-12 flex flex-col cursor-pointer" ref="dashboardCard">
                        <div class="firstFade">
                            <h2 class="hide text-4xl font-bold mt-4">Predictive Dashboard</h2>
                        </div>
                        <div class="secondFade mt-auto">
                            <p class="hide text-gray-600">A predictive dashboard that analyses your order history and
                                inventory needs, helping you optimize your supply chain and reduce waste.</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>

        <!-- When Not Logged In -->
        <section class="border-bottom" id="features" v-else>
            <div class="grid grid-cols-1 md:grid-cols-3 h-screen">
                <!-- AI Sourcing Card -->
                <div class="bg-black text-white px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                    @mouseover="hoverAnimate($event)" @mouseout="hoverOffAnimate($event)">
                    <div>
                        <i class="bi bi-robot text-primary text-3xl"></i>
                        <h2 class="text-4xl font-bold mt-4">AI Sourcing for Buyers</h2>
                    </div>
                    <div class="mt-auto">
                        <p class="hide text-gray-400">AI-powered sourcing helps you find quality ingredients efficiently by
                            analyzing supplier data and sustainability metrics.</p>
                    </div>
                    <div class="col-lg-3">
                        <!-- Picture Placeholder -->
                        <i class="bi bi-robot text-primary fs-1"></i>
                    </div>
                </div>

                <!-- Real-time Database Card -->
                <div class="bg-white px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                    @mouseover="hoverAnimate($event)" @mouseout="hoverOffAnimate($event)">
                    <div>
                        <i class="bi bi-gear-wide-connected text-primary text-3xl"></i>
                        <h2 class="text-4xl font-bold mt-4">Real-time Database for Suppliers</h2>
                    </div>
                    <div class="mt-auto">
                        <p class="hide text-gray-600">Track supplier inventory, metrics, and compliance in real-time through
                            a
                            single dashboard.</p>
                    </div>
                    <div class="col-lg-3">
                        <i class="bi bi-robot text-primary fs-1"></i>
                        <!-- Picture Placeholder -->
                    </div>
                </div>

                <div class="bg-gray-100 px-8 py-12 flex flex-col cursor-pointer transition-opacity hover:opacity-90"
                    @mouseover="hoverAnimate($event)" @mouseout="hoverOffAnimate($event)">
                    <div>
                        <h2 class="text-4xl font-bold mt-4">Automated Payments</h2>
                    </div>
                    <div class="mt-auto">
                        <p class="hide text-gray-600">We use Stripe to handle payments. You can set your payment preferences
                            in your account settings.</p>
                    </div>
                    <div class="col-lg-3">
                        <!-- Picture Placeholder -->
                        <i class="bi bi-robot text-primary fs-1"></i>
                    </div>
                </div>
            </div>

            <!-- Signup Section -->
            <div class="h-screen bg-gray-50">
                <div class="grid grid-cols-1 md:grid-cols-2 h-full">
                    <!-- Restaurant Signup Section (Left) -->
                    <div class="flex flex-col justify-center items-center bg-white p-12 cursor-pointer transition-all hover:bg-gray-50"
                        @click="navigateToSignup('restaurant')">
                        <div class="text-center max-w-lg">
                            <div class="flex justify-center mb-6">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                    stroke="currentColor" class="w-20 h-20 text-black">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M13.5 21v-7.5a.75.75 0 0 1 .75-.75h3a.75.75 0 0 1 .75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349M3.75 21V9.349m0 0a3.001 3.001 0 0 0 3.75-.615A2.993 2.993 0 0 0 9.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 0 0 2.25 1.016c.896 0 1.7-.393 2.25-1.015a3.001 3.001 0 0 0 3.75.614m-16.5 0a3.004 3.004 0 0 1-.621-4.72l1.189-1.19A1.5 1.5 0 0 1 5.378 3h13.243a1.5 1.5 0 0 1 1.06.44l1.19 1.189a3 3 0 0 1-.621 4.72M6.75 18h3.75a.75.75 0 0 0 .75-.75V13.5a.75.75 0 0 0-.75-.75H6.75a.75.75 0 0 0-.75.75v3.75c0 .414.336.75.75.75Z" />
                                </svg>
                            </div>

                            <h3 class="text-4xl font-bold mb-4">Join as a Restaurant</h3>
                            <p class="text-gray-600 mb-6">
                                Access our platform to find the best suppliers and manage your inventory efficiently.
                            </p>
                            <button
                                class="inline-block bg-blue-500 text-white px-8 py-3 rounded-lg hover:bg-blue-600 transition-colors">
                                Sign Up Now
                            </button>
                        </div>
                    </div>

                    <!-- Supplier Signup Section (Right) -->
                    <div class="flex flex-col justify-center items-center bg-black text-white p-12 cursor-pointer transition-all hover:bg-gray-900"
                        @click="navigateToSignup('supplier')">
                        <div class="text-center max-w-lg">
                            <div class="flex justify-center mb-6">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                    stroke="currentColor" class="w-20 h-20 text-white">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
                                </svg>
                            </div>

                            <h3 class="text-4xl font-bold mb-4">Join as a Supplier</h3>
                            <p class="text-gray-400 mb-6">
                                Connect with restaurants and grow your business with our platform.
                            </p>
                            <button
                                class="inline-block bg-blue-500 text-white px-8 py-3 rounded-lg hover:bg-blue-600 transition-colors">
                                Sign Up Now
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
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
        },
        navigateToSignup(type) {
            this.$router.push({
                path: '/login',
                query: {
                    type: type,
                    signup: true,
                    tab: type
                }
            });
        },
        hoverAnimate(event) {
            const target = event.currentTarget;
            const pElement = target.querySelector("p");

            if (pElement) {
                animate(
                    pElement,
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
            }
        },
        hoverOffAnimate(event) {
            const target = event.currentTarget;
            const pElement = target.querySelector("p");

            if (pElement) {
                animate(
                    pElement,
                    {
                        opacity: 0,
                        transform: "translateY(10px)"
                    },
                    {
                        duration: 0.5,
                        easing: [0.17, 0.55, 0.55, 1]
                    }
                );
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
                const cards = ['listingsCard', 'ordersCard', 'checkoutCard', 'inventoryCard', 'paymentsCard', 'dashboardCard'];

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
    opacity: 0;
    transform: translateY(10px);
}
</style>