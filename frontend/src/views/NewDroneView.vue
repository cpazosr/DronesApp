<template>
  <div>
    <h2>Register a New Drone</h2>
    <form @submit.prevent="onRegister" style="display:flex; flex-direction:column; ">
      <select v-model="model_id" required>
        <option disabled value="">Please select a model</option>
        <option v-for="model in droneModels" :key="model.id" :value="model.id">
            {{ model.manufacturer }} - {{ model.model }}
        </option>
      </select>

      <input v-model="serial_number" placeholder="serial number" required/>
      <input v-model="short_name" placeholder="nickname" required/>
      <input v-model="payload" placeholder="payload" />
      <button type="submit">Register</button>
    </form>
    <router-link to="/menu">
        <button>Back</button>
    </router-link>
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
    const model_id = ref("");
    const serial_number = ref("");
    const short_name = ref("");
    const payload = ref("");
    const pilot = ref<{id: uuid; email: string} | null>(null);
    const droneModels = ref<{id: int; manufacturer: string; model: string}[]>([]);
    // feedback mssgs
    const message = ref("");
    const messageColor = ref("green");

    async function getPilot() {
        try {
            const res = await api.get("/pilot");
            console.log(res);
            pilot.value = res.data;
        } catch {
            router.push('/login');
        }
    }

    async function getDroneModels() {
        try {
            const res = await api.get("/drone_models");
            console.log(res);
            droneModels.value = res.data;
        } catch {
            messageColor.value = "red";
            message.value = 'Error fetching drone models';
        }
    }

    async function onRegister() {
        console.log('registering...')
        message.value = "";
        try {
            const res = await api.post("/new_drone", {
                user_id: pilot.id,
                drone_model_id: model_id.value,
                serial_number: serial_number.value,
                short_name: short_name.value,
                payload: payload.value,
            });
            messageColor.value = "green";
            message.value = res.data.message;
            // restart fields for new registration
            serial_number.value = "";
            short_name.value = "";
            payload.value = "";
            router.push("/menu");
        } catch (err: any) {  // post error
            messageColor.value = "red";
            message.value = err.response.data.message;
        }
    }

    onMounted(async() => {
        await getPilot();
        await getDroneModels();
    })
    
    return { model_id, serial_number, short_name, payload, pilot, droneModels, message, messageColor, onRegister}; 
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
