<template>
  <div>
    <h2>
        Manage Flights
        <p><strong>{{ drone_serial_number }} - {{ drone_nickname }}</strong></p>
    </h2>
    <table v-if="flights">
        <thead>
            <tr>
                <th>Type</th>
                <th>Date</th>
                <th>State</th>
                <th>Description</th>
                <th>Fly</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="f in flights" :key="f.id">
                <td>{{ f.type }}</td>
                <td>{{ f.date }}</td>
                <td>{{ f.state }}</td>
                <td class="scrollable-text">{{ f.description }}</td>
                <td>
                    <button @click="fly_drone(drone_id, drone_nickname, drone_serial_number, f.id)">Fly!</button>
                </td>
            </tr>
        </tbody>
    </table>
    <button @click="register_new_flight(drone_id, drone_nickname, drone_serial_number)">New Flight</button>
    <router-link to="/menu">
        <button>Back</button>
    </router-link>
    <p v-if="message" :style="{ color: messageColor }">{{ message }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/api";

export default defineComponent({
  setup() {
    // route params
    const route = useRoute();
    const drone_id = route.params.drone_id as string;
    const drone_nickname = route.params.drone_name as string;
    const drone_serial_number = route.params.serial as string;
    // routing
    const router = useRouter();
    const pilot = ref<{id: string; email: string} | null>(null);
    const flights = ref<{id: string; type: string; date: string, state: string, description: string}[]>([]);
    // feedback mssgs
    const message = ref("");
    const messageColor = ref("green");

    async function getPilot() {
        try {
            const res = await api.get("/pilot");
            pilot.value = res.data;
        } catch {
            router.push('/login');
        }
    }

    async function getFlights() {
        try {
            const res = await api.get("/flights", { params: {drone_id: drone_id} });
            flights.value = res.data;
        } catch {
            messageColor.value = "red";
            message.value = 'Error fetching flights';
        }
    }

    onMounted(async() => {
        await getPilot();
        await getFlights();
    })

    function fly_drone(droneId: string, nickname: string, serial_number: string, flightId: string){
        router.push({name: 'fly', 
        params: {drone_id: droneId, drone_nickname: nickname, serial: serial_number, flight_id: flightId}});
    }

    function register_new_flight(droneId: string, nickname: string, serial_number: string){
        router.push({name: 'new_flight',
            params: {drone_id: droneId, drone_nickname: nickname, serial: serial_number}});
    }
    
    return { drone_id, drone_nickname, drone_serial_number, pilot, flights, message, messageColor, fly_drone, register_new_flight }; 
  },
});
</script>

<style scoped>
input {
  padding: 8px;
}
button {
  padding: 8px;
  cursor: pointer;
}
table {
    width: 100%;
    border-collapse: collapse;
}
th, td {
    padding: 6px;
    text-align: left;
}
.scrollable-text {
  max-width: 200px;
  overflow-x: auto;
  white-space: nowrap;
}
</style>
