import { createApp } from 'vue'
import App from './App.vue'
import Authentication from './components/Authentication/Authentication.vue'
import {createRouter, createWebHashHistory} from 'vue-router'
import Home from './components/Home.vue';
import Chat from './components/chat.vue';
import BuyerDashboard from './components/buyerDashboard.vue';
import FindListings from './components/findListing.vue';
import './firebase.js';



// Define Page Routing
const routes = [
    { path: '/', component: Home },
    { path: '/login', component: Authentication },
    { path: '/chat', component: Chat},



    // Restaurant
    { path: '/buyerDashboard', component: BuyerDashboard},
    // INCLUDE PATH TO OTHER PAGES HERE

    // Supplier
    { path: '/find', component: FindListings},
];

// Create the router instance
const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

// Mount app to html
createApp(App).use(router).mount('#app')