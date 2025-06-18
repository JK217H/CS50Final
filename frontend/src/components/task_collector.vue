<!-- all tasks with no project tag ggo here-->
 <!-- split into, today (), projects, dates (if no project), random whenver (no date, no project) -->
<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import axios from 'axios';

const todoitems = ref([]);
const todoitemsclosed = ref([]);
const toast = useToast();

const toggleStatus = async (taskId) => {
  try {
    const res = await axios.patch(`http://localhost:5000/tasks/task/${taskId}/status`);
    console.log(res.data.message); // "Status toggled successfully"
    // Optionally refresh your tasks list here
    await fetchTasks();
  } catch (error) {
    console.error('Error toggling status:', error);
    toast.error('Failed to toggle status');
  }
}
onMounted (async () => {
  fetchTasks();
});
const fetchTasks = async () => {
try {
        const res = await axios.get(`http://localhost:5000/tasks`);
        todoitems.value = res.data;
        const resc = await axios.get(`http://localhost:5000/tasks/closed`);
        todoitemsclosed.value = resc.data;
    } catch(error) {
        toast.error('Failed to load tasks');
        console.error(error);
    }
};
</script>

<template>  
<div class="flex flex-col items-center min-h-screen">
    <h1 class ="text-2xl font-bold">Taskcollector</h1>
    <div class="flex text-xl font-semibold gap-64 flex-row">
      <h2>Open Tasks</h2> <h2>Closed Tasks</h2>
      </div>
    <div class="flex flex-row gap-8 items-start">
    <table class="border-separate" style="border-spacing: 1rem;">
      <thead>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Date</th>
          <th>Tag</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="todo in todoitems" :key="todo.id">
          <td> {{ todo.title }}</td>
          <td> {{ todo.description }}</td>
          <td> {{ todo.date }}</td>
          <td> {{ todo.tag }}</td>
          <td>
          <input type="checkbox" :checked="todo.status === 'closed'" @change="toggleStatus(todo.id)">
          </td>
        </tr>
      </tbody>
    </table>
    <table class="border-separate" style="border-spacing: 1rem;">
      <thead>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Date</th>
          <th>Tag</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="todo in todoitemsclosed" :key="todo.id">
          <td> {{ todo.title }}</td>
          <td> {{ todo.description }}</td>
          <td> {{ todo.date }}</td>
          <td> {{ todo.tag }}</td>
          <td>
        <input type="checkbox" :checked="todo.status === 'closed'" @change="toggleStatus(todo.id)">
        </td>
        </tr>
      </tbody>
    </table>
    </div>
    </div>
</template>