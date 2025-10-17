import { createRouter, createWebHistory } from 'vue-router';
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import PilotMenu from "@/views/PilotMenu.vue";
import NewDroneView from "@/views/NewDroneView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView},
    { path: '/login', name: 'login', component: LoginView},
    { path: '/register', name: 'register', component: RegisterView},
    { path: '/menu', name: 'menu', component: PilotMenu},
    { path: '/new_drone', name: 'new_drone', component: NewDroneView },
  ],
})

export default router
