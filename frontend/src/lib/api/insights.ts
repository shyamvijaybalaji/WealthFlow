import apiClient from './client';

export interface Insight {
	type: 'success' | 'warning' | 'info' | 'tip';
	title: string;
	message: string;
	icon: string;
}

export const insightsApi = {
	getAll: async (): Promise<Insight[]> => {
		const response = await apiClient.get<Insight[]>('/insights/');
		return response.data;
	}
};
