<template>
  <div style="text-align: left;">
    <h2>
        Welcome <p v-if="pilot"><strong>{{ pilot.email }}</strong>!</p>
    </h2>
    <router-link to="/new_drone">
        <button>New Drone</button>
    </router-link>
    <button @click="logout">Logout</button>
    <h3>Fly your drones</h3>
    <table>
        <thead>
            <tr>
                <th>Nickname</th>
                <th>Serial Number</th>
                <th>Fly</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="d in drones" :key="d.id">
                <td>{{ d.short_name }}</td>
                <td>{{ d.serial_number }}</td>
                <td>
                    <button @click="newFlight(d.id, d.short_name, d.serial_number)">Fly</button>
                </td>
            </tr>
        </tbody>
    </table>
    <p v-if="message" :style="{ color: messageColor }">{{ message }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/api";

export default defineComponent({
    setup() {
        const router = useRouter();
        const pilot = ref<{id: string; email: string} | null>(null);
        const drones = ref<{id: string; short_name: string; serial_number: string}[]>([]);

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

        async function getDrones() {
            try {
                const res = await api.get('/drones');
                drones.value = res.data;
            } catch {
                messageColor.value = "red";
                message.value = 'Error fetching drones';
            }
        }

        async function logout() {
            await api.post("/logout");
            router.push('/');
        }

        onMounted(async() => {
            await getPilot();
            await getDrones();
        });

        function newFlight(droneId: string, nickname: string, serial_number: string){
            router.push({name: 'flights', 
            params: {drone_id: droneId, drone_name: nickname, serial: serial_number}});
        }

        return {pilot, drones, message, messageColor, logout, newFlight};
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
</style>