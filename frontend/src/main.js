import { createApp, defineComponent } from 'vue'
import App from './App.vue'
import Authentication from './components/Authentication/Authentication.vue'
import {createRouter, createWebHashHistory} from 'vue-router'
import Home from './components/Home.vue';
import Chat from './components/chat.vue';
import BuyerDashboard from './components/buyerDashboard.vue';
import BuyerInventory from './components/buyerInvLevel.vue';
import FindListings from './components/Restaurant/FindListings.vue';
import SupplierInventory from './components/Supplier/supplierInventory.vue';
import addIngredientForm from './components/Supplier/addIngredientForm.vue';
import creditScore from './components/creditScore.vue';
// import Test from '@/components/Supplier/Test.vue'; //old table code 
import './firebase.js';
import viewSupplier from './components/Restaurant/viewSupplier.vue';
import Profile from './components/Profile.vue';
import orderHistory from './components/orderHistory.vue';



// Define Page Routing
const routes = [
    { path: '/', component: Home },
    { path: '/login', component: Authentication },
    { path: '/chat/:supplierId/:supplierName', component: Chat},
    { path: '/profile', component: Profile},


<<<<<<< Updated upstream


    // Restaurant
    { path: '/find', component: FindListings},
=======
    // Restaurant
    { path: '/buyerInvLevel', component: BuyerInventory },
>>>>>>> Stashed changes
    { path: '/viewSupplier/:id', name: "viewSupplier",component: viewSupplier},
    { path: '/buyerDashboard', component: BuyerDashboard},
    { path: '/creditScore', component: creditScore},
    { path: '/buyerOrders', component: orderHistory},
    // INCLUDE PATH TO OTHER PAGES HERE

    // Supplier
    { path: '/supplierOrders', component: orderHistory},
    { path: '/supplierInventory', component: SupplierInventory, name: 'supplierInventory'},
    { path: '/addIngredientForm', component: addIngredientForm, name: 'addIngredientForm'},
    // { path: '/test', component: Test},//old table code

];

// Create the router instance
const router = createRouter({
    history: createWebHashHistory(),
    routes,
});


// Mount app to html
createApp(App).use(router).mount('#app')