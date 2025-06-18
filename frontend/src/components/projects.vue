<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useProjectTags } from '@/composables/useProjectTag';

const { projecttags, addTag, fetchTags } = useProjectTags();

const ptag = ref('');
const tasksByTag = reactive({});

const fetchTasksForTag = async (tag) => {
  try {
    const res = await axios.get(`http://localhost:5000/project-tags/ptag/${tag}`);
    tasksByTag[tag] = res.data;
  } catch (error) {
    console.error(`Failed to fetch tasks for tag ${tag}`, error);
    tasksByTag[tag] = [];
  }
};

// render all the tags
//then pass into fetchtasks and fetch all the tags 
onMounted(async () => {
  await fetchTags();
  projecttags.value.forEach(tagObj => {
    fetchTasksForTag(tagObj.tag);
  });
});

const onInput = (e) => {
  e.target.value = e.target.value
    .toUpperCase()
    .replace(/[^A-Z]/g, '')
    .slice(0, 4);
  ptag.value = e.target.value;
};

const handleSubmit = async () => {
  if (ptag.value.length === 4) {
    await addTag(ptag.value)
    await fetchTags();
    await fetchTasksForTag(ptag.value);
    ptag.value = '';
  } else {
    alert('Enter exactly 4 capital letters');
  }
};
</script>

<template>
   <div class="flex flex-col items-center m-4">
  <form @submit.prevent="handleSubmit">
     
    <div>
    <label class ="m-3 text-2xl font-bold" for="ptag">Create Project Tag</label>
    </div>
    <div class="m-3">
    <input
      id="ptag"
      type="text"
      placeholder="4 Capital Letters"
      autocomplete="off"
      maxlength="4"
      v-model="ptag"
      @input="onInput"
      pattern="[A-Z]{4}"
      title="Enter exactly 4 uppercase letters"
    />
    <button type="submit" class="ml-3 px-2 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">Create</button>
  </div>
  </form>
<!-- then you render all the tags via the tasksbytag array which you created above -->
  <div class ="mt-4">
    <h1 class="m-3 text-2xl font-bold ">Projects</h1>
    <ul>
      <li v-for="tagObj in projecttags" :key="tagObj.id">
        <div class ="m-2 text-xl font-semibold ">
        {{ tagObj.tag }}
        </div>
        <ul class="list-disc pl-5">
          <li v-if="!tasksByTag[tagObj.tag] || tasksByTag[tagObj.tag].length === 0">
            No tasks for this project.
          </li>
          <li v-for="task in tasksByTag[tagObj.tag]" :key="task.id">
            {{ task.title }}
          </li>
        </ul>
      </li>
    </ul>
  </div>
  </div>
</template>
