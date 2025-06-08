import { getCollection, type CollectionEntry } from 'astro:content';

export interface PostNavigation {
  previous: CollectionEntry<'posts'> | null;
  next: CollectionEntry<'posts'> | null;
}

export async function getPostNavigation(currentSlug: string): Promise<PostNavigation> {
  const posts = await getCollection('posts');
  
  // Sort posts by date (newest first)
  const sortedPosts = posts.sort((a, b) => 
    new Date(b.data.date).getTime() - new Date(a.data.date).getTime()
  );

  const currentIndex = sortedPosts.findIndex(post => post.slug === currentSlug);
  
  if (currentIndex === -1) {
    return { previous: null, next: null };
  }

  return {
    // Previous post is newer (lower index)
    previous: currentIndex > 0 ? sortedPosts[currentIndex - 1] : null,
    // Next post is older (higher index)
    next: currentIndex < sortedPosts.length - 1 ? sortedPosts[currentIndex + 1] : null
  };
}

export async function getAllTags(): Promise<string[]> {
  const posts = await getCollection('posts');
  const tags = new Set<string>();
  
  posts.forEach(post => {
    if (post.data.tags) {
      post.data.tags.forEach(tag => tags.add(tag));
    }
  });

  return Array.from(tags).sort();
}

export async function getAllCategories(): Promise<string[]> {
  const posts = await getCollection('posts');
  const categories = new Set<string>();
  
  posts.forEach(post => {
    if (post.data.categories) {
      post.data.categories.forEach(category => categories.add(category));
    }
  });

  return Array.from(categories).sort();
}

export function formatDate(date: Date): string {
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

export function calculateReadingTime(content: string): number {
  const wordsPerMinute = 200;
  const words = content.trim().split(/\s+/).length;
  return Math.ceil(words / wordsPerMinute);
}
