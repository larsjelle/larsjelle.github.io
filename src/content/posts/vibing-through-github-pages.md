---
title: Vibing through GitHub Pages
date: 2025-01-08
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

## 🤔 What is Vibe Coding?

Vibe coding is the art of describing what you want in natural language and letting AI do the heavy lifting. It's like being a project manager for your own code - you provide the vision, requirements, and feedback, while the AI handles the implementation details.

---

## 🚀 The Migration Story

My original Jekyll site was a typical developer blog with:

- A few blog posts about cybersecurity

- Basic GitHub Pages deployment

- Outdated Ruby dependencies

- Broken build pipeline

Rather than fixing the Jekyll issues, I decided to completely modernize the stack:

- **Jekyll → Astro** (for better performance and TypeScript support)

- **SCSS → Tailwind CSS** (for utility-first styling)

- **Ruby → Node.js** (for better tooling ecosystem)

- **Manual deployment → GitHub Actions** (for automated CI/CD)

The entire migration took just a few hours of conversation with Claude, and you can check the commit history to see the controlled chaos of AI-generated commits!

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

   - Select "Deploy from a branch"

   - Choose your main branch

---

### Step 2: Getting Started with a Simple Page

Start with a basic `index.html` file to test your setup:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My GitHub Pages Site</title>
</head>
<body>
    <h1>Hello, GitHub Pages!</h1>
    <p>This is my first page.</p>
</body>
</html>
```

Commit and push this file to see your site live at `https://your-username.github.io`.

---

### Step 3: Mandatory Files for GitHub Pages

For a modern static site, you'll typically need:

- **`index.html`** - Your main page

- **`404.html`** - Custom 404 error page

- **`CNAME`** - If using a custom domain

- **`package.json`** - For Node.js dependencies

- **`.github/workflows/deploy.yml`** - GitHub Actions workflow

---

### Step 4: DNS Configuration for Custom Domains

If you want to use a custom domain:

1. Add a `CNAME` file to your repository root with your domain:

   ```plaintext
   yourdomain.com
   ```

2. Configure your DNS provider with these GitHub Pages IPs:

   ```plaintext
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```

3. For CNAME records, point to `your-username.github.io`

---

### Step 5: Setting up GitHub Actions

Create `.github/workflows/deploy.yml` for automated deployment:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "18"
          cache: "npm"
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
        with:
          artifact_name: github-pages
          path: ./dist
```

---

### Step 6: Deployment

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

- Setting up proper SEO meta tags

- Configuring build tools and deployment pipelines

---

## 📚 Lessons Learned

1. **Be specific about your vision** - The more detailed your requirements, the better the results

2. **Iterate incrementally** - Make small changes and test frequently

3. **Review everything** - AI can make mistakes, so always understand what's being implemented

4. **Embrace the unknown** - I learned TypeScript concepts just by reviewing the AI's code

5. **Version control is crucial** - Git allows you to safely experiment and rollback if needed

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

---

*Want to see the chaos? Check out my [commit history](https://github.com/larsjelle/larsjelle.github.io/commits/main) to witness the beautiful mess of AI-guided development in action!*
