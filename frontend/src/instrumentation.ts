import { Configure } from 'nexcore';

export function register() {
  Configure({
    envs: {
      apiUrl: { value: process.env.API_URL, required: true },
    },
    auth: {
      autoRefresh: true,
      onSessionExpired: '/login',
    },
  });
}
