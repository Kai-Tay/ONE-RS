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
    <div class="min-h-screen flex flex-col">
        <!-- Navbar integrated directly in home page -->
        <Navbar v-if="$route.path === '/'" />


        <header class="bg-gray-900 h-screen flex flex-col p-8" @click="scrollToFeatures">
            <!-- Main content container -->
            <div class="flex h-full items-center">
                <!-- Left side content -->
                <div class="w-1/2">
                    <div class="flex-grow flex items-center">
                        <div class="max-w-2xl">
                            <div class="text-4xl md:text-7xl font-bold" ref="titleContainer">
                                <h1 class="text-left text-white mb-2" v-if="isLoggedIn">
                                    Welcome, <br>{{ userName }}
                                </h1>
                                <h1 class="text-4xl md:text-7xl text-left text-white mb-2" v-else ref="mainTitle">
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
                </div>

                <!-- Right side image -->
                <div class="w-1/2 hidden md:flex items-center justify-center overflow-hidden">
                    <img src="../assets/img/oners_homepage.jpeg" 
                        alt="Homepage Image" 
                        style="width: 200%; height: 200%;"
                        class="object-contain rounded-lg shadow-lg"/>
                </div>
            </div>
        </header>

        <!-- When Logged In -->
        <div v-if="isLoggedIn">
            <!-- Supplier -->
            <section id="features" v-if="userType == 'supplier'">
                <div class="grid grid-cols-1 md:grid-cols-3 h-screen">
                    
                    <div class="flex flex-col justify-between bg-black text-white px-5" @click="navigateTo('/supplierInventory')"
                        ref="listingsCard" @mouseover="hoverAnimate($event)" @mouseout="hoverOffAnimate($event)">
                        <h2 class="text-4xl font-bold mt-4">Step 1:
                            <br>Listings
                        </h2>

                        <div class="hidden md:flex justify-center items-center flex-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-40 h-40">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                            </svg>
                        </div>

                        <div class="mb-5">
                            <p class="mb-5">Creating a listing is a breeze! Just snap a photo, write a quick
                                description, and set your price.</p>
                        </div>
                    </div>

                    <div class="flex flex-col justify-between px-5 bg-gray-200" ref="ordersCard" @click="navigateTo('/supplierOrders')" @mouseover="hoverAnimate($event)"
                        @mouseout="hoverOffAnimate($event)">
                        <h2 class="text-4xl font-bold mt-4">Step 2:
                            <br>Receive Orders
                        </h2>

                        <div class="hidden md:flex justify-center items-center flex-1">
                            <svg class="h-40 w-40 text-black"  width="40" height="40" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <polyline points="12 3 20 7.5 20 16.5 12 21 4 16.5 4 7.5 12 3" />  
                                <line x1="12" y1="12" x2="20" y2="7.5" />  
                                <line x1="12" y1="12" x2="12" y2="21" />  
                                <line x1="12" y1="12" x2="4" y2="7.5" />  
                                <line x1="16" y1="5.25" x2="8" y2="9.75" />
                            </svg>
                        </div>

                        <div class="mb-5">
                            <p class="hide mb-5">As a supplier, you receive orders from buyers all over the world.
                                You can accept or reject the order.</p>
                        </div>
                    </div>

                    <div class="flex flex-col h-full px-5" ref="paymentCard" @mouseover="hoverAnimate($event)"
                        @mouseout="hoverOffAnimate($event)">
                        <!-- Top section -->
                        <h2 class="text-4xl font-bold mt-4">Step 3:
                            <br>Checkout
                        </h2>

                        <!-- Middle section with centered icon -->
                        <div class="hidden md:flex justify-center items-center flex-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-40 h-40">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                            </svg>
                        </div>

                        <!-- Bottom section -->
                        <p class="hide mb-5">Ready to get paid? Our secure checkout system ensures timely payments and tracks your sales 
                            history, helping you manage your cash flow efficiently</p>
                    </div>
                </div>

                <div class="h-screen grid grid-rows-2 gap-4" ref="bottomGrid">
                    <div class="bg-gray-100 px-5 flex flex-col cursor-pointer relative group overflow-hidden" ref="aiCard">
                        <div class="firstFade">
                            <h2 class="hide text-4xl font-bold mt-4 flex items-center gap-4">
                                Inventory Management
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25ZM6.75 12h.008v.008H6.75V12Zm0 3h.008v.008H6.75V15Zm0 3h.008v.008H6.75V18Z" />
                                </svg>
                            </h2>
                            <div class="secondFade mt-auto mb-5">
                                <p class="hide text-gray-600">Monitor your inventory levels in real-time. Get insights into your
                                    best-selling items and manage stock efficiently.</p>
                            </div>
                        </div>

                        <div class="md:absolute relative md:bottom-1 md:right-1/4 md:left-1/4 md:w-1/2 md:h-72 hidden md:block md:pt-5">
                            <img src="../assets/img/oners_orderHistory.png" 
                                alt="Homepage Image" 
                                style="width: 250%;"
                                class=" object-cover rounded-lg shadow-lg"/>
                        </div>
                    </div>

                    <div class="bg-gray-100 px-5 flex flex-col cursor-pointer relative group overflow-hidden" ref="dashboardCard">
                        <div class="firstFade">
                            <h2 class="hide text-4xl font-bold mt-4 flex items-center gap-4">Real-Time Chat Translation
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                                </svg>
                            </h2>
                            <div class="secondFade">
                                <p class="hide text-gray-600">Where suppliers and restaurants communicate freely across languages through instant message translation.</p>
                            </div>
                        </div>

                        <div class="md:absolute relative md:bottom-1 md:right-1/4 md:left-1/4 md:w-1/2 md:h-72 hidden md:block md:pt-5">
                            <img src="../assets/img/oners_chat.png" 
                                alt="Homepage Image" 
                                style="width: 250%;"
                                class=" object-cover rounded-lg shadow-lg"/>
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

                        <div class="hidden md:flex justify-center items-center flex-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-40 h-40">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m5.231 13.481L15 17.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v16.5c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Zm3.75 11.625a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                            </svg>
                        </div>
                        
                        <div class="mb-5">
                            <p class="mb-5 ">Find the ingredients needed for your restaurant using our AI Sourcing!
                                All you need to do is to input your ingredients and let the AI do the rest.</p>
                        </div>
                    </div>

                    <div class="flex flex-col justify-between px-5" ref="orderCard" @mouseover="hoverAnimate($event)"
                        @mouseout="hoverOffAnimate($event)">
                        <h2 class="text-4xl font-bold mt-4">Step 2:
                            <br>Place Order
                        </h2>

                        <div class="hidden md:flex justify-center items-center flex-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-40 h-40">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                            </svg>
                        </div>

                        <div class="mb-5">
                            <p class="hide mb-5">As a buyer, you have a credit score to maintain. These will increase for
                                every
                                payment
                                made
                                on time to the supplier. Check your score here!</p>
                        </div>
                    </div>

                    <div class="flex flex-col h-full px-5" ref="paymentCard" @mouseover="hoverAnimate($event)"
                        @mouseout="hoverOffAnimate($event)">
                        <h2 class="text-4xl font-bold mt-4">Step 3:
                            <br>Checkout
                        </h2>

                        <div class="hidden md:flex justify-center items-center flex-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-40 h-40">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                            </svg>
                        </div>
                        
                        <div class="mb-5">
                            <p class="hide mb-5">Are you overbuying ingredients for your business? Use our order optimiser
                                to
                                analyse your
                                order history and plan out your next purchase!</p>
                        </div>
                    </div>
                </div>

                <div class="h-screen grid grid-rows-2 gap-4" ref="bottomGrid">
                    <div class="bg-gray-100 px-5 flex flex-col cursor-pointer relative group overflow-hidden" ref="aiCard">
                        <div class="firstFade">
                            <h2 class="hide text-4xl font-bold mt-4 flex items-center gap-4">AI Sourcing
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m5.231 13.481L15 17.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v16.5c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Zm3.75 11.625a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                                </svg>
                            </h2>
                            <div class="secondFade">
                                <p class="hide text-gray-600">Find the ingredients needed for your restaurant using our AI
                                    Sourcing!
                                    All you need to do is to input your ingredients and let the AI do the rest.</p>
                            </div>
                        </div>

                        <div class="md:absolute relative md:bottom-1 md:right-1/4 md:left-1/4 md:w-1/2 md:h-72 hidden md:block md:pt-5">
                            <img src="../assets/img/oners_findSuppliers.png" 
                                alt="Homepage Image" 
                                style="width: 250%;"
                                class="object-cover rounded-lg shadow-lg"/>
                        </div>
                    </div>

                    <div class="bg-gray-100 px-5 flex flex-col cursor-pointer relative group overflow-hidden" ref="dashboardCard">
                        <div class="firstFade">
                            <h2 class="hide text-4xl font-bold mt-4 flex items-center gap-4">Predictive Dashboard
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6 20.25h12A2.25 2.25 0 0 0 20.25 18V6A2.25 2.25 0 0 0 18 3.75H6A2.25 2.25 0 0 0 3.75 6v12A2.25 2.25 0 0 0 6 20.25Z" />
                                </svg>
                            </h2>
                            <div class="secondFade">
                                <p class="hide text-gray-600">A predictive dashboard that analyses your order history and
                                    inventory needs, helping you optimize your supply chain and reduce waste.</p>
                            </div>
                        </div>

                        <div class="md:absolute relative md:bottom-1 md:right-1/4 md:left-1/4 md:w-1/2 md:h-72 hidden md:block md:pt-5">
                            <img src="../assets/img/oners_dashboard.png" 
                                alt="Homepage Image" 
                                style="width: 250%;"
                                class="object-cover rounded-lg shadow-lg"/>
                        </div>
                    </div>
                </div>
            </section>
        </div>

        <!-- When Not Logged In -->
        <section class="border-bottom" id="features" v-else>
            <div class="grid grid-cols-1 md:grid-cols-3 min-h-screen">
                <!-- AI Sourcing Card -->
                <div class="bg-black text-white px-5 flex flex-col justify-between"
                    @mouseover="hoverAnimate($event)" @mouseout="hoverOffAnimate($event)">
                    <div>
                        <h2 class="text-4xl font-bold mt-4">AI Sourcing for Buyers</h2>
                    </div>

                    <div class="hidden md:flex justify-center items-center flex-1 h-96 flex-grow flex-shrink">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-40 h-40">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m5.231 13.481L15 17.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v16.5c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Zm3.75 11.625a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                        </svg>
                    </div>

                    <div class="mb-5">
                        <p class="hide text-gray-400 md:text-xl">AI-powered sourcing helps you find quality ingredients efficiently by
                            analyzing supplier data and sustainability metrics.</p>
                    </div>
                </div>

                <!-- Real-time Database Card -->
                <div class="bg-white px-5 flex flex-col justify-between"
                    @mouseover="hoverAnimate($event)" @mouseout="hoverOffAnimate($event)">
                    <div>
                        <h2 class="text-4xl font-bold mt-4">Inventory Management for Suppliers</h2>
                    </div>

                    <div class="hidden md:flex justify-center items-center flex-1 h-96 flex-grow flex-shrink">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-40 h-40">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
                        </svg>
                    </div>

                    <div class="mb-5">
                        <p class="hide text-gray-600 md:text-xl">Track supplier inventory, metrics, and compliance in real-time through
                            a
                            single dashboard.</p>
                    </div>
                </div>

                <div class="bg-gray-100 px-5 flex flex-col justify-between"
                    @mouseover="hoverAnimate($event)" @mouseout="hoverOffAnimate($event)">
                    <div>
                        <h2 class="text-4xl font-bold mt-4">Real-time Chat Translation</h2>
                    </div>

                    <div class="hidden md:flex justify-center items-center flex-1 h-96 flex-grow flex-shrink">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-40 h-40">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                        </svg>
                    </div>

                    <div class="mb-5">
                        <p class="hide text-gray-600 md:text-xl">Chat in your language, understood in theirs. Real-time translation for seamless business communication.</p>
                    </div>
                </div>
            </div>

            

            <!-- Signup Section -->
            <div class="h-fit md:h-screen grid grid-rows-2 md:grid-rows-1 md:grid-cols-2">
                <!-- Restaurant Signup Section (White Background) -->
                <div class="py-12 flex flex-col items-center justify-center bg-white cursor-pointer" 
                    @click="navigateToSignup('restaurant')">
                    <div class="text-center px-4">
                        <div class="flex justify-center mb-6">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-20 h-20 text-black">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M13.5 21v-7.5a.75.75 0 0 1 .75-.75h3a.75.75 0 0 1 .75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349M3.75 21V9.349m0 0a3.001 3.001 0 0 0 3.75-.615A2.993 2.993 0 0 0 9.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 0 0 2.25 1.016c.896 0 1.7-.393 2.25-1.015a3.001 3.001 0 0 0 3.75.614m-16.5 0a3.004 3.004 0 0 1-.621-4.72l1.189-1.19A1.5 1.5 0 0 1 5.378 3h13.243a1.5 1.5 0 0 1 1.06.44l1.19 1.189a3 3 0 0 1-.621 4.72M6.75 18h3.75a.75.75 0 0 0 .75-.75V13.5a.75.75 0 0 0-.75-.75H6.75a.75.75 0 0 0-.75.75v3.75c0 .414.336.75.75.75Z" />
                            </svg>
                        </div>

                        <h3 class="text-4xl font-bold mb-4">Join as a Restaurant</h3>
                        <p class="text-gray-600 mb-6 ">
                            Access our platform to find the best suppliers and manage your inventory efficiently.
                        </p>
                        <button
                            class="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-600 transition-colors">
                            Sign Up
                        </button>
                    </div>
                </div>

                <!-- Supplier Signup Section (Right) -->
                <div class="py-12 flex flex-col items-center justify-center bg-black text-white cursor-pointer" 
                    @click="navigateToSignup('supplier')">
                    <div class="text-center px-4">
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
                            class="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-600 transition-colors">
                            Sign Up
                        </button>
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

        // Check auth state immediately when component is created
        if (!sessionStorage.getItem('uid')) {
            this.$router.push('/');
            return;
        }
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
        }, 
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
        window.addEventListener('storage', () => {
        if (!sessionStorage.getItem('uid')) {
            this.$router.push('/');
            }
        });

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