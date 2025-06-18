<!-- all single days are clickable -->
 <script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import dayjs from 'dayjs';

const ctasks = ref([]);
// null cuz intentional empty value 
const selectedDate = ref(null);


const filteredTasks = computed (() => {
    if (!selectedDate.value) return [];
// if selectedDate.value is none return an expty array, needed when loading the page and no day is selected 

//first I get today, I then change the date to of today to the seleted day and then format it the right way 
  const selectedDateStr = currentDate.value
    .date(selectedDate.value)
    .format('YYYY-MM-DD');
//the task arrow function is filter syntax which basically means select all the tasks where task.date == that certain string 
  return ctasks.value.filter(task => task.date === selectedDateStr);


});


// returns today as default 
const currentDate = ref(dayjs()); 

// Start of thhe month as a dayjs object 
const startOfMonth = computed (() => currentDate.value.startOf('month'));

// Get the number of days in a month 
const daysInMonth = computed(() => currentDate.value.daysInMonth());

// gets the starting day of the month sunday , monday etc. (sunday = 0)
const startDay = computed(() => startOfMonth.value.day());

//create a calendar days array 
const calendarDays = computed(() => {
    const daysArray =[];

    
    for (let i = 0; i < startDay.value; i++) {
        daysArray.push(null);
    } 

    for (let day = 1; day <= daysInMonth.value; day++) {
        daysArray.push(day);
    }
    
    return daysArray;
});

const goToPrevMonth = () => {
  currentDate.value = currentDate.value.subtract(1, 'month');
};

const goToNextMonth = () => {
  currentDate.value = currentDate.value.add(1, 'month');
};


onMounted (async () => {
    try {
        const res = await axios.get('http://localhost:5000/calendar-tasks')
        ctasks.value = res.data;
    } catch(error) {
        console.error('Failed to load tasks', error)
    }
});
</script>


<template>
  <!-- Whole page wrapper -->
  <div>

    <!-- Flex row: calendar on left -->
    <div class="flex flex-row">
      <!-- Calendar block -->
      <div>
        <div class="calendar-header">
          <button class="ml-1 px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700" @click="goToPrevMonth">Prev</button>
          <button class="ml-2 px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700" @click="goToNextMonth">Next</button>
          <h2 class="m-2 font-semibold text-xl text-blue-800">{{ currentDate.format('MMMM YYYY') }}</h2>
        </div>

        <div class="calendar">
          <div class="weekdays">
            <div v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="day" class="weekday">
              {{ day }}
            </div>
          </div>

          <div class="days-grid">
            <div
              v-for="(day, index) in calendarDays"
              :key="index"
              class="day-cell"
              :class="{ 'empty': day === null, 'selected': selectedDate === day }"
              @click="day && (selectedDate = day)"
            >
              {{ day || '' }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ✅ Task section centered relative to page -->
    <div class="max-w-xl mx-auto md:-mt-72 text-center">
      <div class="tasks-list">
        <h2 v-if="filteredTasks.length" class="text-xl font-semibold mb-2">Tasks for {{ selectedDate }}</h2>
        <ul v-if="filteredTasks.length">
          <li v-for="task in filteredTasks" :key="task.id">
            {{ task.title }}
          </li>
        </ul>
        <p v-else class="text-gray-600 italic">No tasks for this day.</p>
      </div>
    </div>
  </div>
</template>


<style scoped>
.calendar {
  width: 300px;
  user-select: none;
}
.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  font-weight: bold;
  text-align: center;
  margin-bottom: 8px;
}
.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}
.day-cell {
  height: 40px;
  line-height: 40px;
  text-align: center;
  border-radius: 4px;
}
.day-cell.empty {
  background: #f0f0f0;
}
/* the :not(.empty) is taking out all the daycell empty classes because they are also daycell classes :not is just party of css syntax to exclude */
.day-cell:not(.empty):hover {
  background: #d0ebff;
  cursor: pointer;
}
</style>
