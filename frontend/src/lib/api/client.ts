import axios from 'axios';
import { browser } from '$app/environment';
import { PUBLIC_API_URL } from '$env/static/public';

const apiClient = axios.create({
	baseURL: PUBLIC_API_URL,
	headers: {
		'Content-Type': 'application/json'
	}
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
	if (browser) {
		const token = localStorage.getItem('token');
		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
		}
	}
	return config;
});

// Handle 401 errors (redirect to login)
apiClient.interceptors.response.use(
	(response) => response,
	(error) => {
		if (error.response?.status === 401 && browser) {
			localStorage.removeItem('token');
			localStorage.removeItem('user');
			window.location.href = '/login';
		}
		return Promise.reject(error);
	}
);

export default apiClient;
