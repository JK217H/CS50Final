import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import ProjectsView from '@/views/ProjectsView.vue';
import CalendarView from '@/views/CalendarView.vue';
import TaskCollectorView from '@/views/TaskCollectorView.vue';
import Editor from '@/views/EditorView.vue';
// Define your routes here
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
    {
    path: '/projects',
    name: 'Projects',
    component: ProjectsView,
  },
    {
    path: '/calendar',
    name: 'Calendar',
    component: CalendarView,
  },
    {
    path: '/taskcollector',
    name: 'TaskCollector',
    component: TaskCollectorView,
  },
    {
    path: '/task',
    name: 'Editor',
    component: Editor,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
