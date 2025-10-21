<template>
  <div>
    <h2>Register a New Flight</h2>
    <form @submit.prevent="onRegister" style="display:flex; flex-direction:column; ">
      <select v-model="state" required>
        <option disabled value="">Please select a model</option>
        <option value="planned">Planned</option>
        <option value="finished">Finished</option>
        <option value="cancelled">Cancelled</option>
      </select>
      <select v-model="type" required>
        <option disabled value="">Please select a type</option>
        <option value="waypoints">Waypoints</option>
        <option value="recording">Record flight</option>
        <option value="polygons">Polygons</option>
      </select>
      <button type="submit">Register</button>
    </form>
    <button @click="newFlight(drone_id, drone_nickname, drone_serial_number)">Back</button>
    <p v-if="message" :style="{ color: messageColor }">{{ message }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/api";

export default defineComponent({
  setup() {
    const route = useRoute();
    const drone_id = route.params.drone_id as string;
    const drone_nickname = route.params.drone_nickname as string;
    const drone_serial_number = route.params.serial as string;
    const router = useRouter();
    const type = ref("");
    const state = ref("");
    const pilot = ref<{id: string; email: string} | null>(null);
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

    async function onRegister() {
        console.log('registering...')
        message.value = "";
        try {
            const res = await api.post("/new_flight", {
                drone_id: drone_id,
                pilot_id: pilot.value?.id,
                state: state.value,
                type: type.value,
            });
            messageColor.value = "green";
            message.value = res.data.message;
            newFlight(drone_id, drone_nickname, drone_serial_number);
        } catch (err: any) {  // post error
            messageColor.value = "red";
            message.value = err.response.data.message;
        }
    }

    onMounted(async() => {
        await getPilot();
    })

    function newFlight(droneId: string, nickname: string, serial_number: string){
        router.push({name: 'flights', 
        params: {drone_id: droneId, drone_name: nickname, serial: serial_number}});
    }
    
    return { drone_id, drone_nickname, drone_serial_number, type, state, message, messageColor, onRegister, newFlight}; 
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
</style>
