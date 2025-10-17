<template>
  <div style="text-align: center;">
    <h2>Welcome</h2>
    <div style="display: flex; gap:120px; justify-content: center;">
      <router-link to="/login">
        <button>Login</button>
      </router-link>
      <router-link to="/register">
        <button>Register</button>
      </router-link>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({});
</script>