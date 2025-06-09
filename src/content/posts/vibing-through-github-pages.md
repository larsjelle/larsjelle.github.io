---
title: Vibing through GitHub Pages
date: 2025-06-09
categories: 
  - Tech
tags: 
  - vibecoding
  - github-pages
  - software-development
  - typescript
  - astro
  - tailwind
  - github-copilot
  - claude-sonnet
excerpt: How I completely rebuilt my website using AI assistance without writing a single line of code myself - a journey through TypeScript, Astro, and the power of vibe coding.
author: Lars van Blitterswijk
draft: false
---


**⚠️ Disclaimer:** *This post was written entirely by AI (Claude Sonnet 4) and may contain mistakes or inaccuracies. Always verify technical information before implementing.*

---

## 🌟 The Journey Begins

Two years ago, I set up a simple blog using the **Chirpy Jekyll theme**. Fast forward to today, I discovered my entire GitHub pipeline was completely broken due to outdated dependencies and version conflicts. Instead of debugging the mess, I decided to take a different approach: let AI completely rebuild my website from scratch.

What followed was an incredible journey of "vibe coding" - where I guided **Claude Sonnet 4** through **GitHub Copilot's agent mode** to migrate my entire project from Jekyll to a modern **TypeScript** and **Tailwind CSS** stack using **Astro**. The best part? I didn't write a single line of code myself, despite not knowing TypeScript at all (I just know we use it at my company).

---

## 🎯 Prerequisites & What You'll Need

Before diving into your own AI-assisted development journey, here's what you'll need:

### Essential Tools
- **GitHub account** with basic Git knowledge
- **VS Code** or any modern code editor
- **Terminal/command line** access
- **AI assistant** (GitHub Copilot, Claude, or similar)

### Helpful Background Knowledge
- Basic understanding of web development concepts
- Experience with Git version control

### What's Not Required
- TypeScript knowledge (I don't know it either!)
- Astro framework experience
- Advanced build tool configuration
- Complex deployment pipeline setup

---

## 📋 Solution Preview: What We'll Build

By the end of this journey, you'll have created a blog with:

### 🏗️ **Technical Stack**

```plain
Frontend: Astro + TypeScript + Tailwind CSS
Content: Markdown with type-safe collections
Deployment: GitHub Actions → GitHub Pages
Styling: Utility-first CSS with dark mode
DNS: Custom domain (optional)
```

### 🚀 **Key Features**

- **Lightning-fast performance** - Sub-second page loads
- **Type-safe content management** - Prevent errors at build time
- **Responsive design** - Looks great on all devices
- **Automated deployments** - Push to deploy in minutes
- **Reading time calculation** - Automatic word count analysis
- **Post navigation** - Previous/next post links
- **Tag and category system** - Dynamic content organization

### 🎨 **User Experience**

- Clean, modern design with excellent typography
- Instant page transitions with prefetching
- Accessible navigation with keyboard support
- Mobile-optimized reading experience
- Fast search functionality

### 💰 **Cost**

- **$0** - Completely free using GitHub Pages
- **AI assistance**: Free tier available for most AI tools

---

## 🤔 What is Vibe Coding?

Vibe coding is the art of describing what you want in natural language and letting AI do the heavy lifting. It's like being a project manager for your own code - you provide the vision, requirements, and feedback, while the AI handles the implementation details.

Think of it as **architectural programming** where you:

- Define the high-level structure and requirements
- Describe the desired user experience
- Provide feedback on AI-generated solutions
- Iterate through conversations rather than keystrokes

This approach democratizes development, allowing non-developers to build sophisticated applications by focusing on **what** they want rather than **how** to implement it.

---

## 🚀 The Migration Story

My original Jekyll site was a typical template based blog with:

- Basic GitHub Pages deployment
- Outdated Ruby dependencies
- Broken build pipeline
- Manual content management

Rather than fixing the Jekyll issues, I decided to give GitHub Copilot Agent mode a try and completely modernized the stack:

- **Jekyll → Astro** (for better performance and TypeScript support)
- **SCSS → Tailwind CSS** (for utility-first styling)
- **Ruby → Node.js** (for better tooling ecosystem)
- **Manual deployment → GitHub Actions** (for automated CI/CD)
- **Loose content → Type-safe collections** (for better content validation)

The entire migration took just a few hours of conversation with Claude, and you can check the commit history to see the controlled chaos of AI-generated commits!

### Technical Architecture Decisions

The AI made several sophisticated architectural decisions based on my repository analysis:

**1. Content Collections with Zod Validation**: Implemented type-safe frontmatter validation using Astro's content collections:

```typescript
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
```

**2. Utility-First CSS with Tailwind**: Custom configuration with dark mode support and typography extensions for optimal reading experience.

**3. Blog Utilities**: Smart helper functions for post navigation, reading time calculation, and tag/category management.

---

## 🛠️ Getting Started: Your Own Vibe Coding Journey

Want to build your own GitHub Pages site using AI assistance? Here's a step-by-step tutorial:

### Step 1: Setting up the GitHub Repository

1. Create a new repository named `your-username.github.io`

2. Clone it locally:

   ```bash
   git clone https://github.com/your-username/your-username.github.io.git
   cd your-username.github.io
   ```

3. Enable GitHub Pages in your repository settings:

   - Go to **Settings → Pages**
   - Select "GitHub Actions" as the source (not "Deploy from a branch")
   - Choose your main branch

---

### Step 2: Project Initialization with Modern Tools

Start by initializing a modern Node.js project with Astro:

```bash
# Initialize package.json
npm init -y

# Install Astro and essential dependencies
npm create astro@latest . --template minimal --typescript

# Add additional integrations
npm install @astrojs/tailwind @astrojs/mdx @astrojs/sitemap @tailwindcss/typography
```

This creates the foundation for a type-safe, performant static site similar to the one powering this blog.

---

### Step 3: Essential Configuration Files

Your project needs several key configuration files that the AI helped create for this site:

**`astro.config.mjs`** - Main Astro configuration with integrations:

```javascript
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://your-username.github.io',
  output: 'static',
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
  integrations: [tailwind(), mdx(), sitemap()]
});
```

**`tailwind.config.mjs`** - Tailwind CSS configuration with typography:

```javascript
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: 'none',
            color: 'inherit',
            lineHeight: '1.7'
          }
        }
      }
    }
  },
  plugins: [require('@tailwindcss/typography')]
};
```

---

### Step 4: Content Collections Setup

Create type-safe content collections exactly like this blog uses:

**`src/content/config.ts`**:

```typescript
import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    excerpt: z.string().optional(),
    date: z.date(),
    categories: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    author: z.string().default('Your Name'),
    draft: z.boolean().default(false),
    image: z.string().optional(),
  }),
});

export const collections = { posts };
```

This ensures all blog posts follow a consistent structure and prevents content errors at build time.

---

### Step 5: Blog Utilities Implementation

Create utility functions for blog functionality in `src/utils/blog.ts`:

```typescript
import { getCollection, type CollectionEntry } from 'astro:content';

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

export async function getPostNavigation(currentSlug: string) {
  const posts = await getCollection('posts');
  const sortedPosts = posts.sort((a, b) => 
    new Date(b.data.date).getTime() - new Date(a.data.date).getTime()
  );
  
  const currentIndex = sortedPosts.findIndex(post => post.slug === currentSlug);
  
  return {
    previous: currentIndex > 0 ? sortedPosts[currentIndex - 1] : null,
    next: currentIndex < sortedPosts.length - 1 ? sortedPosts[currentIndex + 1] : null
  };
}
```

---

### Step 6: Advanced GitHub Actions Workflow

The AI created a sophisticated deployment workflow with error handling and optimizations:

**`.github/workflows/pages-deploy.yml`**:

```yaml
name: Deploy Astro site to Pages

on:
  push:
    branches: ["main", "master"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "18"
          cache: "npm"
          
      - name: Setup Pages
        uses: actions/configure-pages@v5
        with:
          enablement: true
          
      - name: Install dependencies
        run: npm ci
        env:
          CI: true
          NODE_ENV: production
      
      - name: Build with Astro
        run: |
          set -e
          echo "Building Astro site..."
          npm run build
          echo "Build completed successfully"
        env:
          CI: true
          NODE_ENV: production
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Key features of this workflow:**

- **Separate build/deploy jobs** for better organization and debugging
- **Environment variables** for production optimization
- **Error handling** with `set -e` to catch build failures
- **Artifact caching** for faster subsequent builds
- **Concurrency control** to prevent deployment conflicts

The AI also created an alternative workflow (`.github/workflows/pages-deploy-alternative.yml`) that runs only on manual dispatch, providing a fallback deployment option.

1. Push your changes to the main branch

2. GitHub Actions will automatically build and deploy your site

3. Monitor the **Actions tab** for build status

4. Your site will be live at `https://your-username.github.io`

---

## 🌐 The Power of AI-Assisted Development

What amazed me most about this experience was how Claude understood not just the technical requirements, but also the design intent. I could say things like "make the sidebar more modern" or "add a dark mode toggle" and it would implement exactly what I envisioned.

The AI handled complex tasks like:

- Setting up TypeScript configurations
- Implementing responsive design with Tailwind
- Creating dynamic category and tag systems
- Configuring build tools and deployment pipelines

### What the AI Actually Built

Looking at the final codebase, the AI created a sophisticated architecture:

**Advanced PostLayout Component**: A fully-featured blog post layout with:

- Reading time calculation
- Post navigation (previous/next)
- Responsive design with dark mode
- SEO-optimized metadata
- Structured markup for accessibility

**Type-Safe Blog Utilities**: Smart helper functions including:

- `getAllTags()` and `getAllCategories()` for dynamic taxonomy
- `formatDate()` for consistent date formatting
- `calculateReadingTime()` based on word count analysis
- `getPostNavigation()` for chronological post browsing

**Production-Ready GitHub Actions**: Two deployment workflows:

- **Main workflow**: Automatic deployment on push to main/master
- **Alternative workflow**: Manual deployment trigger for emergency situations
- Both include proper error handling, environment variables, and artifact management

**Tailwind Configuration**: Custom typography settings with:

- Dark mode support via class strategy
- Extended typography plugin for optimal reading
- Responsive design tokens
- Custom color schemes for light/dark themes

---

## 📚 Lessons Learned

1. **Be specific about your vision** - The more detailed your requirements, the better the results

2. **Iterate incrementally** - Make small changes and test frequently

3. **Review everything** - AI can make mistakes, so always understand what's being implemented

4. **Embrace the unknown** - I learned TypeScript concepts just by reviewing the AI's code

5. **Version control is crucial** - Git allows you to safely experiment and rollback if needed

### Technical Insights Gained

Through this AI-assisted migration, I gained deep understanding of:

**Modern Static Site Generation**: How Astro's island architecture provides optimal performance while maintaining developer experience

**TypeScript in Practice**: Real-world usage of type definitions, interfaces, and generic types for content management

**Build Pipeline Optimization**: How GitHub Actions can be configured for reliable, fast deployments with proper error handling

**CSS Architecture**: The benefits of utility-first CSS with Tailwind over traditional component-based stylesheets

**Content Strategy**: How type-safe content collections prevent errors and improve content management workflows

---

## 🎉 The Result

The final website is a modern, fast, and maintainable blog built with:

- **Astro** for static site generation
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **GitHub Actions** for CI/CD
- **Responsive design** that works on all devices

All of this was achieved through natural language conversations with AI, proving that you don't need to be a coding expert to build professional-quality websites.

---

## 🏁 Conclusion

Vibe coding with AI assistants like Claude Sonnet 4 and GitHub Copilot has democratized web development. You can now focus on the creative and strategic aspects while letting AI handle the implementation details.

Whether you're a seasoned developer looking to speed up your workflow or a complete beginner wanting to build your first website, AI-assisted development opens up incredible possibilities.

The future of coding isn't about replacing developers - it's about amplifying human creativity and making technology accessible to everyone who has ideas worth sharing.

**The paradigm shift is profound:**

- **From syntax to intent** - Focus on what you want to build, not how
- **From implementation to iteration** - Spend time refining ideas, not debugging code
- **From technical barriers to creative expression** - Ideas become the limiting factor, not coding skills
- **From individual craft to collaborative intelligence** - Human creativity amplified by AI capabilities

**Key takeaways for aspiring AI-assisted developers:**

1. **Start with clear vision** - Know what you want to achieve
2. **Communicate iteratively** - Build through conversation and feedback
3. **Embrace learning** - Let AI teach you through implementation
4. **Stay curious** - Question everything and understand the "why"
5. **Think architecturally** - Focus on user experience and system design

**For experienced developers:**

AI doesn't replace programming skills - it amplifies them. You can now:

- Explore unfamiliar technologies without deep learning curves
- Focus on architecture and user experience
- Automate repetitive tasks and boilerplate code

Whether you're a seasoned developer looking to accelerate your workflow, a designer wanting to implement your own ideas, or a complete beginner with a vision worth sharing, AI-assisted development opens up possibilities.

The tools are here. The capabilities are proven. The only question is: what will you build?

---

*Want to see the beautiful chaos in action? Check out my [commit history](https://github.com/larsjelle/larsjelle.github.io/commits/main) to witness the controlled madness of AI-guided development. Every commit tells the story of human intent meeting artificial intelligence - a collaboration that created something neither could have built alone.*

*Ready to start your own vibe coding journey? The conversation begins with a simple question: "What do you want to build today?"*
