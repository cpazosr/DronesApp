<template>
  <div>
    <h2>Add mission details</h2>
    <form @submit.prevent="onSubmit" style="display:flex; flex-direction:column; ">
      <textarea v-model="description" rows="10" cols="50" placeholder="Enter flight details...">
      </textarea>
      <br/>
      <button type="submit">Update</button>
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
    const flight_id = route.params.flight_id as string;
    const router = useRouter();
    const description = ref("");
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

    async function onSubmit() {
        console.log('updating...')
        message.value = "";
        try {
            const res = await api.post("/update_flight", {
              flight_id: flight_id,
              description: description.value,
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
    
    return { drone_id, drone_nickname, drone_serial_number, flight_id, description, message, messageColor, onSubmit, newFlight}; 
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
