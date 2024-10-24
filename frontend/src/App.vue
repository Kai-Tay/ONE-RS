<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
</script>

<template>
  <Navbar />
    <RouterView></RouterView>
</template>

<style>
body{
  background-color: whitesmoke;
}
</style>