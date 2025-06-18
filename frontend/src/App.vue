<script setup>
import Navbar from '@/components/navbar.vue';
import { RouterView } from 'vue-router';

</script>


<template>
  <div class="min-h-screen p-5" style="background-color: #cfe9e6;">
    <Navbar />
    <RouterView />
  </div>
</template>