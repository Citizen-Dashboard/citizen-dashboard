import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [sveltekit()],
    server: {
        host: '0.0.0.0',  // This allows external access
        port: 5173
    },
    env: {
        VITE_SEARCH_API_PORT: process.env.SEARCH_API_PORT,
    },
});