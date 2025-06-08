// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://larsjelle.github.io',
  markdown: {
    syntaxHighlight: 'shiki',
    shikiConfig: {
      theme: 'github-dark',
      themes: {
        light: 'github-light',
        dark: 'github-dark'
      },
      wrap: true
    },
    gfm: true,
    smartypants: true
  },
  integrations: [
    tailwind(),
    mdx(),
    sitemap()
  ]
});