import apiClient from './client';

export interface DashboardSummary {
	total_balance: number;
	total_accounts: number;
	total_transactions: number;
	total_budget: number;
	total_spent: number;
	budget_remaining: number;
	recent_transactions: RecentTransaction[];
	expense_by_category: ExpenseByCategory[];
}

export interface RecentTransaction {
	id: number;
	amount: number;
	description: string;
	transaction_type: string;
	transaction_date: string;
	merchant: string | null;
}

export interface ExpenseByCategory {
	category_name: string;
	category_icon: string;
	category_color: string;
	total: number;
}

export const dashboardApi = {
	getSummary: async (): Promise<DashboardSummary> => {
		const response = await apiClient.get<DashboardSummary>('/dashboard/summary');
		return response.data;
	}
};
