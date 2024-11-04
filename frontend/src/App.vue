<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div class="bg-slate-50 h-dvh">
    <Navbar />
    <RouterView></RouterView>
  </div>
</template>
