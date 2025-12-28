import apiClient from './client';

export interface SavingsGoal {
	id: number;
	user_id: number;
	goal_name: string;
	target_amount: number;
	current_amount: number;
	deadline: string | null;
	icon: string | null;
	created_at: string;
	updated_at: string;
}

export interface SavingsGoalWithProgress extends SavingsGoal {
	progress_percentage: number;
	remaining: number;
}

export interface SavingsGoalCreate {
	goal_name: string;
	target_amount: number;
	current_amount?: number;
	deadline?: string | null;
	icon?: string | null;
}

export interface SavingsGoalUpdate {
	goal_name?: string;
	target_amount?: number;
	current_amount?: number;
	deadline?: string | null;
	icon?: string | null;
}

export const savingsGoalsApi = {
	getAll: async (): Promise<SavingsGoalWithProgress[]> => {
		const response = await apiClient.get<SavingsGoalWithProgress[]>('/savings-goals/');
		return response.data;
	},

	create: async (data: SavingsGoalCreate): Promise<SavingsGoal> => {
		const response = await apiClient.post<SavingsGoal>('/savings-goals/', data);
		return response.data;
	},

	get: async (id: number): Promise<SavingsGoalWithProgress> => {
		const response = await apiClient.get<SavingsGoalWithProgress>(`/savings-goals/${id}`);
		return response.data;
	},

	update: async (id: number, data: SavingsGoalUpdate): Promise<SavingsGoal> => {
		const response = await apiClient.put<SavingsGoal>(`/savings-goals/${id}`, data);
		return response.data;
	},

	delete: async (id: number): Promise<void> => {
		await apiClient.delete(`/savings-goals/${id}`);
	}
};
