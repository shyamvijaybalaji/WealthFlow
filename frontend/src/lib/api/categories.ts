import apiClient from './client';

export interface Category {
	id: number;
	user_id: number | null;
	name: string;
	category_type: string;
	icon: string | null;
	color: string | null;
	is_system: boolean;
	created_at: string;
	updated_at: string;
}

export const categoriesApi = {
	getAll: async (): Promise<Category[]> => {
		const response = await apiClient.get<Category[]>('/categories/');
		return response.data;
	}
};
