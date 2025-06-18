<!-- one singular to-do list item-->
<!-- you have: description, title, reocurring?, tag?, day? -->
 <script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useProjectTags } from '@/composables/useProjectTag'
const { projecttags, fetchTags } = useProjectTags()
import { useToast } from 'vue-toastification';
const allTasks = ref([]);
const toast = useToast();

const searchQuery = ref('')


const selectedTask = ref(null)

const fetchAllTasks = async () => {
  const res = await axios.get('http://localhost:5000/tasks')
  allTasks.value = res.data
}

const matchingTasks = computed(() => {
  if (!searchQuery.value) return []
  return allTasks.value.filter(task =>
    task.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})


const selectTask = async (task) => {
  const res = await axios.get(`http://localhost:5000/tasks/${task.id}`)

  selectedTask.value = res.data
}
const updateTask = async () => {
  try {
    await axios.patch(`http://localhost:5000/tasks/${selectedTask.value.id}`, selectedTask.value)
    toast.success("Task updated!")
    selectedTask.value = ''
     await fetchAllTasks()
  } catch (error) {
    console.error("Failed to update", error)
  }
}
const deleteTask = async () => {
  try {
    await axios.delete(`http://localhost:5000/tasks/${selectedTask.value.id}`, selectedTask.value)
    toast.success("Task deleted!")
    selectedTask.value = ''
    await fetchAllTasks()
  } catch(error) {
    console.error("Failed to delete Task", error)
  }
}
const editingTag = ref(null)
const newTagName = ref('')

const startEditTag = (tag) => {
    editingTag.value = tag    
    newTagName.value = tag
}
const cancelEditTag = () => {
    editingTag.value = null
    newTagName.value = ''
}

const confirmEditTag = async (oldTag) => {
    try {
        if ( newTagName.value.length === 4)
        {
        await axios.patch (`http://localhost:5000/project-tags/${oldTag}`, {
            new_tag: newTagName.value
        })
        }
        else {
          toast.error("Tag must be 4 letters long")
          return console.error("Tag must be 4 letters long")
        }
        if (selectedTask.value?.tag === oldTag) {
            selectedTask.value.tag = newTagName.value
        }
        await fetchTags()
        await fetchAllTasks()
        cancelEditTag()
        toast.success('Tag renamed!')
    } catch (error) {
        console.error('Rename failed', error)
        toast.error('Failed to rename tag')
    }
}

const deleteTag = async (tag) => {
    const confirmed = confirm (`Delete tag "${tag}" from all tasks?`)
    if (!confirmed) return
    try {
        await axios.delete(`http://localhost:5000/project-tags/${tag}`)
        if (selectedTask.value?.tag === tag){
            selectedTask.value.tag = ''
        }
        await fetchTags()
        await fetchAllTasks()
        toast.success ('Tag deleted')
    } catch (error) {
        console.error('Failed to delete tag', error)
        toast.error ('Failed to delete')
    }
}


onMounted(() => {
    fetchAllTasks()
    fetchTags()
})

</script>

<template>  
<div class="flex flex-row gap-5 justify-center">
<div>
  <div class="w-72 space-y-4">
    <h2 class="text-xl font-semibold">Search for a Task</h2>

<!-- User types search here -->
<input class="w-full px-2 py-1 border rounded" v-model="searchQuery" placeholder="Search tasks by title..." />

<ul v-if="matchingTasks.length &&!selectedTask">
  <li 
    v-for="task in matchingTasks" 
    :key="task.id"
    @click="selectTask(task)"
    style="cursor: pointer;"
  >
    {{ task.title }}
  </li>
</ul>
</div>
<!-- Show results -->


    <!-- then show each properties old value with the ability to change -->
<div v-if="selectedTask">
  <h3 class="mt-1 mb-1">Edit Task: {{ selectedTask.title }}</h3>
  <form @submit.prevent="updateTask">
    <div class="w-72 space-y-4">
  <div>
    <label class="block mb-1 font-medium">Title:</label>
    <input required v-model="selectedTask.title" class="w-full px-2 py-1 border rounded" />
  </div>

  <div>
    <label class="block mb-1 font-medium">Description:</label>
    <input v-model="selectedTask.description" class="w-full px-2 py-1 border rounded" />
  </div>

  <div>
    <label class="block mb-1 font-medium">Date:</label>
    <input type="date" v-model="selectedTask.date" class="w-full px-2 py-1 border rounded" />
  </div>

  <div>
    <label class="block mb-1 font-medium">Tag:</label>
    <select v-model="selectedTask.tag" class="w-full px-2 py-1 border rounded">
      <option value="">No Tag</option>
      <option v-for="tag in projecttags" :key="tag.id" :value="tag.tag">{{ tag.tag }}</option>
    </select>
  </div>

  <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded">Save Changes</button>
  <button type="button" @click="deleteTask(selectedTask.value)" class="w-full bg-blue-500 text-white py-2 rounded">Delete Task</button>
</div>
  </form>
</div>
</div>
<div>
 <!-- project tag manager-->
  <h2 class="text-xl font-semibold">Project Tag Manager</h2>
  <div class="flex justify-center">
  <ul>
    <li v-for="tag in projecttags" :key="tag.tag">
        <!-- when editing task -->
        <template v-if="editingTag !== tag.tag">
            {{ tag.tag }}
            <button class="m-1" @click="startEditTag(tag.tag)">Edit</button>
            <button class="m-1" @click="deleteTag(tag.tag)">Delete</button>
      </template>
      <!-- when not editing task -->
        <template v-else>
            <input v-model="newTagName" />
            <button class ="m-1"@click="confirmEditTag(tag.tag)">Save</button>
            <button class ="m-1" @click="cancelEditTag">Cancel</button>
      </template>
    </li>
  </ul>
  </div>
</div>
</div>
</template>