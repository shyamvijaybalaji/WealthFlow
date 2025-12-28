import apiClient from './client';

export interface Transaction {
	id: number;
	user_id: number;
	account_id: number;
	category_id: number | null;
	amount: number;
	description: string;
	merchant: string | null;
	transaction_type: string;
	transaction_date: string;
	tags: string[] | null;
	notes: string | null;
	created_at: string;
	updated_at: string;
}

export interface TransactionCreate {
	account_id: number;
	category_id?: number | null;
	amount: number;
	description: string;
	merchant?: string | null;
	transaction_type: string;
	transaction_date: string;
	tags?: string[] | null;
	notes?: string | null;
}

export interface TransactionUpdate {
	account_id?: number;
	category_id?: number | null;
	amount?: number;
	description?: string;
	merchant?: string | null;
	transaction_type?: string;
	transaction_date?: string;
	tags?: string[] | null;
	notes?: string | null;
}

export const transactionsApi = {
	getAll: async (params?: {
		skip?: number;
		limit?: number;
		start_date?: string;
		end_date?: string;
		account_id?: number;
		category_id?: number;
	}): Promise<Transaction[]> => {
		const response = await apiClient.get<Transaction[]>('/transactions/', { params });
		return response.data;
	},

	create: async (data: TransactionCreate): Promise<Transaction> => {
		const response = await apiClient.post<Transaction>('/transactions/', data);
		return response.data;
	},

	get: async (id: number): Promise<Transaction> => {
		const response = await apiClient.get<Transaction>(`/transactions/${id}`);
		return response.data;
	},

	update: async (id: number, data: TransactionUpdate): Promise<Transaction> => {
		const response = await apiClient.put<Transaction>(`/transactions/${id}`, data);
		return response.data;
	},

	delete: async (id: number): Promise<void> => {
		await apiClient.delete(`/transactions/${id}`);
	}
};
