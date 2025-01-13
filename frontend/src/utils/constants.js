import axios from "axios";

export const baseURL = process.env.REACT_APP_BASE_URL || 'http://localhost:8000/';

const apiClient = axios.create ({
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json',
    }
})

export default apiClient;
