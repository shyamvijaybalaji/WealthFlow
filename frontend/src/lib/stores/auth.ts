import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import type { User } from '$lib/types/user';
import { authApi } from '$lib/api/auth';

interface AuthState {
	user: User | null;
	token: string | null;
	loading: boolean;
}

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>({
		user: null,
		token: null,
		loading: true
	});

	return {
		subscribe,
		init: async () => {
			if (!browser) return;

			const token = localStorage.getItem('token');
			const userStr = localStorage.getItem('user');

			if (token && userStr) {
				try {
					const user = JSON.parse(userStr);
					set({ user, token, loading: false });
				} catch {
					localStorage.removeItem('token');
					localStorage.removeItem('user');
					set({ user: null, token: null, loading: false });
				}
			} else {
				set({ user: null, token: null, loading: false });
			}
		},
		login: async (email: string, password: string) => {
			const tokenResponse = await authApi.login(email, password);

			// Store token BEFORE calling getCurrentUser so the interceptor can use it
			if (browser) {
				localStorage.setItem('token', tokenResponse.access_token);
			}

			const user = await authApi.getCurrentUser();

			if (browser) {
				localStorage.setItem('user', JSON.stringify(user));
			}

			set({ user, token: tokenResponse.access_token, loading: false });
		},
		register: async (email: string, password: string, full_name?: string) => {
			await authApi.register({ email, password, full_name });
			// Auto-login after registration
			const tokenResponse = await authApi.login(email, password);

			// Store token BEFORE calling getCurrentUser so the interceptor can use it
			if (browser) {
				localStorage.setItem('token', tokenResponse.access_token);
			}

			const user = await authApi.getCurrentUser();

			if (browser) {
				localStorage.setItem('user', JSON.stringify(user));
			}

			set({ user, token: tokenResponse.access_token, loading: false });
		},
		logout: () => {
			if (browser) {
				localStorage.removeItem('token');
				localStorage.removeItem('user');
			}
			set({ user: null, token: null, loading: false });
		}
	};
}

export const auth = createAuthStore();
