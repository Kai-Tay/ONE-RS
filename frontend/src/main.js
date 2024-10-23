import { createApp } from 'vue'
import App from './App.vue'
import Authentication from './components/Authentication/Authentication.vue'
import {createRouter, createWebHashHistory} from 'vue-router'
import Home from './components/Home.vue';
import Chat from './components/chat.vue';
import BuyerDashboard from './components/buyerDashboard.vue';
import FindListings from './components/Restaurant/FindListings.vue';
import SupplierInventory from './components/Supplier/supplierInventory.vue';
import addIngredientForm from './components/Supplier/addIngredientForm.vue';
import Test from '@/components/Supplier/Test.vue'; //old table code 
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
    { path: '/supplierInventory', component: SupplierInventory, name: 'supplierInventory'},
    { path: '/addIngredientForm', component: addIngredientForm, name: 'addIngredientForm'},
    { path: '/test', component: Test},//old table code

];

// Create the router instance
const router = createRouter({
    history: createWebHashHistory(),
    routes,
});


// Mount app to html
createApp(App).use(router).mount('#app')