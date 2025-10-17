<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="onLogin" style="display:flex; flex-direction:column;">
      <input v-model="email" type="email" placeholder="e-mail" required />
      <input v-model="password" type="password" placeholder="password" required />
      <button type="submit">Login</button>
    </form>
    <p v-if="message" :style="{ color: messageColor }">{{ message }}</p>
    <p style="margin-top:14px;">
      Not registered?
      <router-link to="/register">Register</router-link>
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/api";

export default defineComponent({
  setup() {
    const router = useRouter();
    const email = ref("");
    const password = ref("");
    const message = ref("");
    const messageColor = ref("green");

    async function onLogin() {
        console.log('logging in...');
        message.value = "";

        try {
            const res = await api.post("/login", {
                email: email.value,
                password: password.value,
            });
            messageColor.value = "green";
            message.value = res.data.message;
            // only clean password, keep same email
            password.value = "";
            router.push('/menu');
        } catch (err: any) {
            messageColor.value = "red";
            message.value = err.response.data.message;
        }
    }
    
    return { email, password, message, messageColor, onLogin};
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
