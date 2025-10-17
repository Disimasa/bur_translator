import { sveltekit } from '@sveltejs/kit/vite'
import { defineConfig } from 'vite'

export default defineConfig(({ mode }) => ({
	plugins: [
		sveltekit()
	],
	build: {
		target: 'es2020',
		minify: 'esbuild',
		cssMinify: true,
		sourcemap: mode !== 'production',
		chunkSizeWarningLimit: mode === 'production' ? 500 : 1000,
	},
	// Предварительная оптимизация зависимостей
	optimizeDeps: {
		include: ['svelte-sonner', 'svelte-loading-spinners']
	},
	// Настройки сервера разработки
	server: {
		fs: {
			allow: ['..']
		}
	}
}))
