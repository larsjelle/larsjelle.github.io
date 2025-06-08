import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    excerpt: z.string().optional(),
    date: z.date(),
    categories: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    author: z.string().default('Lars van Blitterswijk'),
    draft: z.boolean().default(false),
    image: z.string().optional(),
  }),
});

export const collections = {
  posts,
};
