import axios from 'axios';

// Set up the base URL based on the environment (local or production)
const API = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api',
});

// Attach token dynamically for all requests
API.interceptors.request.use((config) => {
    const token = localStorage.getItem('token'); // Retrieve token from localStorage
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Exported API functions
export const register = async (data) => {
    try {
        const response = await API.post('/register', data);
        return response.data;
    } catch (error) {
        console.error('Registration Error:', error.response?.data || error.message);
        throw error;
    }
};

export const login = async (data) => {
    try {
        const response = await API.post('/login', data);
        console.log('API Response:', response); // Debugging
        return response.data;
    } catch (error) {
        console.error('Login API Error:', error.response?.data || error.message);
        throw error;
    }
};


export const getPosts = async () => {
    try {
        const response = await API.get('/posts');
        return response.data;
    } catch (error) {
        console.error('Get Posts Error:', error.response?.data || error.message);
        throw error;
    }
};

export const createPost = async (data) => {
    try {
        const response = await API.post('/posts', data);
        return response.data;
    } catch (error) {
        console.error('Create Post Error:', error.response?.data || error.message);
        throw error;
    }
};

export default API;
