<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { useProjectTags } from '@/composables/useProjectTag';
import axios from 'axios';

const { projecttags, fetchTags } = useProjectTags();

function getTodayET() {
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/New_York',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });

  const [{ value: month }, , { value: day }, , { value: year }] = formatter.formatToParts(new Date());

  return `${year}-${month}-${day}`;
}

const today = ref(getTodayET());

const todoitems = ref([]);
const todoitemsclosed = ref([]);
const toast = useToast();

const fetchTasks = async () => {
try {
        const res = await axios.get(`http://localhost:5000/tasks/date/active/${today.value}`);
        todoitems.value = res.data;
        const resc = await axios.get(`http://localhost:5000/tasks/date/closed/${today.value}`);
        todoitemsclosed.value = resc.data;
    } catch(error) {
        toast.error('Failed to load tasks');
        console.error(error);
    }
};

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

const todoitem = reactive({
    title: '',
    description: '',
    tag: '',
    date:'',
    status: '',
});


onMounted(async () => {
    fetchTasks();
    fetchTags();
});





const handleSubmit = async () => {
    const newTask = {
        title: todoitem.title,
        description: todoitem.description,
        tag: todoitem.tag,
        date: todoitem.date,
        status:"active",
    };
try {
    const res = await axios.post('http://localhost:5000/task', newTask)
    Object.assign(todoitem, { title: '', description: '', tag: '', date: '' });   
    const newId = res.data.id;
   // router.push(`/task/${newId}`);
    console.log(newId)
    toast.success('Task added succesfully!');
    fetchTasks();
} catch(error){
    console.error('Error adding task:', error);
    toast.error('Failed to add task');
}
};
// have some kind of checker if there wasn't an error then do this 


</script>

<template>  
  <div class="flex flex-col items-center m-4">
    <h1 class="m-3 text-4xl font-bold">Adding a task</h1>

    <div class="w-full max-w-xl">  <!-- container with max width -->

      <form @submit.prevent="handleSubmit">
        <div class="p-3">
          <label for="tasktitle" class="block text-xl">Title</label>
          <input required v-model="todoitem.title" type="text" name="tasktitle" id="tasktitle" placeholder="Add task" autocomplete="off" class="w-full" />
        </div>
        <div class="p-3">
          <label for="taskdescription" class="block text-xl">Description</label>
          <input v-model="todoitem.description" id="taskdescription" type="text" name="taskdescription" placeholder="Add task description" autocomplete="off" class="w-full" />
        </div>
        <div class="p-3">
          <label for="tasktag" class="block text-xl">Project-Tag</label>
          <select v-model="todoitem.tag" name="tasktag" id="tasktag" class="w-full">
            <option value="">No Tag</option>
            <option v-for="tag in projecttags" :key="tag" :value="tag.tag">{{ tag.tag }}</option>
          </select>
        </div>
        <div class="p-3">
          <label for="taskdate" class="block text-xl">Date</label>
          <input v-model="todoitem.date" type="date" name="taskdate" id="taskdate" class="w-full" />
        </div>
        <div class="p-3 flex justify-start">
          <button type="submit" class="text-xl px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Add Task</button>
        </div>
      </form>

      <div class="mt-8">  <!-- spacing from form -->
        <h1 class="text-xl font-semibold mb-2">To-Do-List</h1>
        <ul class="list-disc pl-5">
          <li v-for="todo in todoitems" :key="todo.id">
            {{ todo.title }}
            <input type="checkbox" :checked="todo.status === 'closed'" @change="toggleStatus(todo.id)" class="ml-2" />
          </li>
        </ul>
      </div>

      <div class="mt-8">
        <h1 class="text-xl font-semibold mb-2">Closed Tasks</h1>
        <ul class="list-disc pl-5">
          <li v-for="todo in todoitemsclosed" :key="todo.id">
            {{ todo.title }}
            <input type="checkbox" :checked="todo.status === 'closed'" @change="toggleStatus(todo.id)" class="ml-2" />
          </li>
        </ul>
      </div>

    </div>
  </div>
</template>
