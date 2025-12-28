import apiClient from './client';

export interface Investment {
	id: number;
	user_id: number;
	asset_type: string;
	symbol: string;
	quantity: number;
	purchase_price: number;
	current_price: number | null;
	purchase_date: string;
	created_at: string;
	updated_at: string;
}

export interface InvestmentWithROI extends Investment {
	total_cost: number;
	current_value: number;
	profit_loss: number;
	roi_percentage: number;
}

export interface PortfolioSummary {
	total_invested: number;
	current_value: number;
	total_profit_loss: number;
	roi_percentage: number;
	investments_by_type: Record<string, { count: number; total_value: number }>;
}

export interface InvestmentCreate {
	asset_type: string;
	symbol: string;
	quantity: number;
	purchase_price: number;
	current_price?: number | null;
	purchase_date: string;
}

export interface InvestmentUpdate {
	asset_type?: string;
	symbol?: string;
	quantity?: number;
	purchase_price?: number;
	current_price?: number | null;
	purchase_date?: string;
}

export const investmentsApi = {
	getAll: async (): Promise<InvestmentWithROI[]> => {
		const response = await apiClient.get<InvestmentWithROI[]>('/investments/');
		return response.data;
	},

	getSummary: async (): Promise<PortfolioSummary> => {
		const response = await apiClient.get<PortfolioSummary>('/investments/summary');
		return response.data;
	},

	create: async (data: InvestmentCreate): Promise<Investment> => {
		const response = await apiClient.post<Investment>('/investments/', data);
		return response.data;
	},

	get: async (id: number): Promise<InvestmentWithROI> => {
		const response = await apiClient.get<InvestmentWithROI>(`/investments/${id}`);
		return response.data;
	},

	update: async (id: number, data: InvestmentUpdate): Promise<Investment> => {
		const response = await apiClient.put<Investment>(`/investments/${id}`, data);
		return response.data;
	},

	delete: async (id: number): Promise<void> => {
		await apiClient.delete(`/investments/${id}`);
	}
};
