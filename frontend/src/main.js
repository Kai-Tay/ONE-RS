import { createApp } from 'vue'
import App from './App.vue'
import Authentication from './components/Authentication.vue'
import {createRouter, createWebHashHistory} from 'vue-router'
import Home from './components/Home.vue';


// Define Page Routing
const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Authentication }
    // INCLUDE PATH TO OTHER PAGES HERE
];

// Create the router instance
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// Mount app to html
createApp(App).use(router).mount('#app')