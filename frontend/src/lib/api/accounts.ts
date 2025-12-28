import apiClient from './client';

export interface Account {
	id: number;
	user_id: number;
	account_name: string;
	account_type: string;
	balance: number;
	currency: string;
	created_at: string;
	updated_at: string;
}

export interface AccountCreate {
	account_name: string;
	account_type: string;
	balance?: number;
	currency?: string;
}

export interface AccountUpdate {
	account_name?: string;
	account_type?: string;
	balance?: number;
	currency?: string;
}

export const accountsApi = {
	getAll: async (): Promise<Account[]> => {
		const response = await apiClient.get<Account[]>('/accounts/');
		return response.data;
	},

	create: async (data: AccountCreate): Promise<Account> => {
		const response = await apiClient.post<Account>('/accounts/', data);
		return response.data;
	},

	get: async (id: number): Promise<Account> => {
		const response = await apiClient.get<Account>(`/accounts/${id}`);
		return response.data;
	},

	update: async (id: number, data: AccountUpdate): Promise<Account> => {
		const response = await apiClient.put<Account>(`/accounts/${id}`, data);
		return response.data;
	},

	delete: async (id: number): Promise<void> => {
		await apiClient.delete(`/accounts/${id}`);
	}
};
