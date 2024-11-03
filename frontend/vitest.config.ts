/// <reference types="vitest" />
import { fileURLToPath } from 'node:url'
import { mergeConfig, defineConfig, configDefaults } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      reporters: ['default', 'junit'],
      outputFile: './test-results.xml',
      globals: true,
      environment: 'jsdom',
      setupFiles: './setupTests.ts', 
      exclude: [...configDefaults.exclude, 'e2e/**'],
      root: fileURLToPath(new URL('./', import.meta.url)),
      include: ['./**/*.{test,spec}.{js,ts,jsx,tsx}'],
      coverage: {
        provider: 'istanbul',
        reporter: ['text', 'lcov', 'json', 'html'],
        reportsDirectory: './coverage',
        exclude: ['node_modules/', 'tests/'], 
    }
  }

}));

