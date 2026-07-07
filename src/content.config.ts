import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  // Astro 7 content layer: load Markdown from src/content/posts
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    excerpt: z.string().optional(),
    date: z.coerce.date(),
    categories: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    author: z.string().default('Lars van Blitterswijk'),
    draft: z.boolean().default(false),
    image: z.string().optional(),
  }),
});

export const collections = { posts };
