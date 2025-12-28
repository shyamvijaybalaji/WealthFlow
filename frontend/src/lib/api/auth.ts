import apiClient from './client';
import type { User, TokenResponse, RegisterRequest } from '$lib/types/user';

export const authApi = {
	login: async (email: string, password: string): Promise<TokenResponse> => {
		const formData = new FormData();
		formData.append('username', email);
		formData.append('password', password);

		const response = await apiClient.post<TokenResponse>('/auth/login', formData, {
			headers: { 'Content-Type': 'multipart/form-data' }
		});
		return response.data;
	},

	register: async (data: RegisterRequest): Promise<User> => {
		const response = await apiClient.post<User>('/auth/register', data);
		return response.data;
	},

	getCurrentUser: async (): Promise<User> => {
		const response = await apiClient.get<User>('/auth/me');
		return response.data;
	}
};
