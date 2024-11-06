<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div class="bg-neutral-100 min-h-screen pb-4">
    <Navbar v-if="$route.path !== '/'" />
    <RouterView></RouterView>
  </div>
</template>
