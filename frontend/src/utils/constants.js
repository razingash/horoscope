import axios from "axios";

export const baseURL = process.env.REACT_APP_BASE_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create ({
    baseURL: process.env.REACT_APP_BASE_URL ? `${process.env.REACT_APP_BASE_URL}/api/` : `${baseURL}/api/`,
    headers: {
        'Content-Type': 'application/json',
    }
})

export default apiClient;
