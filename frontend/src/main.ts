import './assets/main.css'      // source styling

// registration
import { createApp } from 'vue';    // basic vue App
import App from './App.vue';        // take custom App
import router from './router';      // take custom router

const app = createApp(App);
app.use(router);
app.mount('#app');
