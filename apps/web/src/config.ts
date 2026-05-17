/** OpenBerg Terminal — web app configuration from env vars. */

export const API_URL = import.meta.env.VITE_API_URL || '/api';

export const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === 'true';
