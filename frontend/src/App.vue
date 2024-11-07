<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
import Footer from './components/footer.vue';
</script>

<template>
  <div class="bg-neutral-100 min-h-screen">
    <Navbar v-if="$route.path !== '/'" />
    <RouterView></RouterView>
    <Footer />
  </div>
</template>
