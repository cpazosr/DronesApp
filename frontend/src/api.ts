import axios from 'axios';
// axios connects front and backend

const api = axios.create({
    baseURL: "http://127.0.0.1:5000",  // running in localhost
    headers: {"Content-Type" : "application/json" },    // communication with json
    withCredentials: true,  // session cookies enabled
});

export default api;

// by importing this file you can call methods like api.post(endpoint, ...) -> api.post("/register",...)