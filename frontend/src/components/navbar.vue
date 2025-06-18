<script setup>
import { RouterLink } from 'vue-router';

</script>

<template>  
   <div class="flex items-center p-4">
    <div class="flex gap-6 text-2xl ml-auto mr-auto font-bold p-5"  style="background-color: #d0cfe9">
        <RouterLink to="/">Home </RouterLink>
        <RouterLink to="/projects">Projects </RouterLink>
        <RouterLink to="/calendar">Calendar </RouterLink>
        <RouterLink to="/taskcollector">Taskcollector</RouterLink>
        <RouterLink to="/task">Editor</RouterLink>
    </div>
    </div>
</template>