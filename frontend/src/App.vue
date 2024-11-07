<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
import Footer from './components/footer.vue';
</script>

<template>
  <div class="bg-neutral-100 min-h-screen flex flex-col">
    <Navbar v-if="$route.path !== '/'" />
    <div class="flex-grow">
      <RouterView />
    </div>
    <Footer />
  </div>
</template>
