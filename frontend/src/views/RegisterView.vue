<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="onRegister" style="display:flex; flex-direction:column; ">
      <input v-model="email" type="email" placeholder="e-mail" required/>
      <input v-model="password" type="password" placeholder="password" required/>
      <input v-model="full_name" placeholder="full name"/>
      <input v-model="institution" placeholder="Volateq" required/>
      <input v-model="birthdate" type="date" placeholder="dd/mm/yyyy" required/>
      <button type="submit">Register</button>
    </form>
    <p v-if="message" :style="{ color: messageColor }">{{ message }}</p>    <!-- only if message -->
    <p style="margin-top: 14px;">
      Already registered?
      <router-link to="/login">Login</router-link>
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
    const email = ref("");   // ref - reactive values | variable is const, values are variable
    const password = ref("");
    const full_name = ref("");
    const institution = ref("");
    const birthdate = ref("");
    // feedback mssgs
    const message = ref("");
    const messageColor = ref("green");

    async function onRegister() {
        console.log('registering...')
        message.value = "";
        try {
            const res = await api.post("/register", {   // send values and collect response
                email: email.value,
                password: password.value,
                full_name: full_name.value,
                institution: institution.value,
                birthdate: birthdate.value,
            });
            messageColor.value = "green";
            message.value = res.data.message;  // response message
            // restart fields for new registration
            email.value = "";
            password.value = "";
            full_name.value = "";
            institution.value = "";
            birthdate.value = "";
            router.push("/menu");
        } catch (err: any) {  // post error
            messageColor.value = "red";
            message.value = err.response.data.message;
        }
    }
    
    // mandatory to return all reactive values and function
    return { email, password, full_name, institution, birthdate, message, messageColor, onRegister}; 
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
