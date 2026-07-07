// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://larsjelle.nl',
  output: 'static',
  adapter: undefined,
  // Old /about page retired into the single-page landing.
  redirects: {
    '/about': '/#about'
  },
  markdown: {
    syntaxHighlight: 'shiki',
    shikiConfig: {
      // Single dark theme to match the always-dark site.
      theme: 'github-dark',
      wrap: true
    }
  },
  integrations: [
    mdx(),
    sitemap()
  ],
  vite: {
    plugins: [tailwindcss()]
  }
});