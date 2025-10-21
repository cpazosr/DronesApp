import { createRouter, createWebHistory } from 'vue-router';
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import PilotMenu from "@/views/PilotMenu.vue";
import NewDroneView from "@/views/NewDroneView.vue";
import ManageFlightsView from "@/views/ManageFlightsView.vue";
import NewFlightView from "@/views/NewFlightView.vue";
import FlyView from "@/views/FlyView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView},
    { path: '/login', name: 'login', component: LoginView},
    { path: '/register', name: 'register', component: RegisterView},
    { path: '/menu', name: 'menu', component: PilotMenu},
    { path: '/new_drone', name: 'new_drone', component: NewDroneView },
    { path: '/flights/:drone_id/:drone_name/:serial', 
      name: 'flights', component: ManageFlightsView, props: true },
    { path: '/new_flight/:drone_id/:drone_name/:serial', 
      name: 'new_flight', component: NewFlightView, props: true},
    { path: '/fly/:drone_id/:drone_name/:serial/:flight_id',
      name: 'fly', component: FlyView, props: true },
  ],
})

export default router
