import axios from "axios";

export const baseURL = process.env.REACT_APP_BASE_URL || 'http://127.0.0.1:8000/api/';

const apiClient = axios.create ({
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json',
    }
})

export default apiClient;
