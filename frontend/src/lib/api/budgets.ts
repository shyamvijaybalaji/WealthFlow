import apiClient from './client';

export interface Budget {
	id: number;
	user_id: number;
	category_id: number;
	amount: number;
	period: string;
	alert_threshold: number;
	start_date: string;
	created_at: string;
	updated_at: string;
}

export interface BudgetWithSpending extends Budget {
	spent: number;
	remaining: number;
	percentage: number;
	status: 'ok' | 'warning' | 'exceeded';
}

export interface BudgetCreate {
	category_id: number;
	amount: number;
	period: string;
	alert_threshold?: number;
	start_date: string;
}

export interface BudgetUpdate {
	category_id?: number;
	amount?: number;
	period?: string;
	alert_threshold?: number;
	start_date?: string;
}

export const budgetsApi = {
	getAll: async (): Promise<BudgetWithSpending[]> => {
		const response = await apiClient.get<BudgetWithSpending[]>('/budgets/');
		return response.data;
	},

	create: async (data: BudgetCreate): Promise<Budget> => {
		const response = await apiClient.post<Budget>('/budgets/', data);
		return response.data;
	},

	get: async (id: number): Promise<BudgetWithSpending> => {
		const response = await apiClient.get<BudgetWithSpending>(`/budgets/${id}`);
		return response.data;
	},

	update: async (id: number, data: BudgetUpdate): Promise<Budget> => {
		const response = await apiClient.put<Budget>(`/budgets/${id}`, data);
		return response.data;
	},

	delete: async (id: number): Promise<void> => {
		await apiClient.delete(`/budgets/${id}`);
	}
};
