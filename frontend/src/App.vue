<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div class="bg-slate-50 min-h-screen">
    <Navbar v-if="$route.path !== '/'" />
    <RouterView></RouterView>
  </div>
</template>
