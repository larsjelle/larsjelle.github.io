---
title: Categories
icon: fas fa-folder-open
order: 1
layout: page
---

<div class="categories">
  <h2>Post Categories</h2>
  
  <div class="categories-grid">
    <div class="category-card">
      <div class="category-header">
        <h3 class="category-name">
          <a href="#tech-security" class="category-link">
            Tech & Security
          </a>
        </h3>
        <span class="post-count">{% assign tech_posts = site.categories['tech-security'] %}{{ tech_posts.size | default: 0 }} post{% if tech_posts.size != 1 %}s{% endif %}</span>
      </div>
      
      <div class="category-posts" id="tech-security">
        {% assign tech_posts = site.categories['tech-security'] %}
        {% if tech_posts.size > 0 %}
          {% for post in tech_posts limit: 5 %}
            <article class="category-post">
              <div class="post-meta">
                <time datetime="{{ post.date | date_to_xmlschema }}">
                  {{ post.date | date: "%b %d, %Y" }}
                </time>
              </div>
              <h4 class="post-title">
                <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
              </h4>
              {% if post.excerpt %}
                <p class="post-excerpt">{{ post.excerpt | strip_html | truncate: 100 }}</p>
              {% endif %}
            </article>
          {% endfor %}
          
          {% if tech_posts.size > 5 %}
            <div class="view-more">
              <a href="{{ '/categories/tech-security' | relative_url }}" class="view-more-link">
                View all {{ tech_posts.size }} posts →
              </a>
            </div>
          {% endif %}
        {% else %}
          <p class="no-posts-message">No posts in this category yet. Stay tuned for content about cybersecurity, programming, and technology!</p>
        {% endif %}
      </div>
    </div>

    <div class="category-card">
      <div class="category-header">
        <h3 class="category-name">
          <a href="#lifestyle" class="category-link">
            Lifestyle
          </a>
        </h3>
        <span class="post-count">{% assign lifestyle_posts = site.categories['lifestyle'] %}{{ lifestyle_posts.size | default: 0 }} post{% if lifestyle_posts.size != 1 %}s{% endif %}</span>
      </div>
      
      <div class="category-posts" id="lifestyle">
        {% assign lifestyle_posts = site.categories['lifestyle'] %}
        {% if lifestyle_posts.size > 0 %}
          {% for post in lifestyle_posts limit: 5 %}
            <article class="category-post">
              <div class="post-meta">
                <time datetime="{{ post.date | date_to_xmlschema }}">
                  {{ post.date | date: "%b %d, %Y" }}
                </time>
              </div>
              <h4 class="post-title">
                <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
              </h4>
              {% if post.excerpt %}
                <p class="post-excerpt">{{ post.excerpt | strip_html | truncate: 100 }}</p>
              {% endif %}
            </article>
          {% endfor %}
          
          {% if lifestyle_posts.size > 5 %}
            <div class="view-more">
              <a href="{{ '/categories/lifestyle' | relative_url }}" class="view-more-link">
                View all {{ lifestyle_posts.size }} posts →
              </a>
            </div>
          {% endif %}
        {% else %}
          <p class="no-posts-message">No posts in this category yet. Coming soon: thoughts on life, personal experiences, and more!</p>
        {% endif %}
      </div>
    </div>

    <div class="category-card">
      <div class="category-header">
        <h3 class="category-name">
          <a href="#recipes" class="category-link">
            Recipes
          </a>
        </h3>
        <span class="post-count">{% assign recipe_posts = site.categories['recipes'] %}{{ recipe_posts.size | default: 0 }} post{% if recipe_posts.size != 1 %}s{% endif %}</span>
      </div>
      
      <div class="category-posts" id="recipes">
        {% assign recipe_posts = site.categories['recipes'] %}
        {% if recipe_posts.size > 0 %}
          {% for post in recipe_posts limit: 5 %}
            <article class="category-post">
              <div class="post-meta">
                <time datetime="{{ post.date | date_to_xmlschema }}">
                  {{ post.date | date: "%b %d, %Y" }}
                </time>
              </div>
              <h4 class="post-title">
                <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
              </h4>
              {% if post.excerpt %}
                <p class="post-excerpt">{{ post.excerpt | strip_html | truncate: 100 }}</p>
              {% endif %}
            </article>
          {% endfor %}
          
          {% if recipe_posts.size > 5 %}
            <div class="view-more">
              <a href="{{ '/categories/recipes' | relative_url }}" class="view-more-link">
                View all {{ recipe_posts.size }} posts →
              </a>
            </div>
          {% endif %}
        {% else %}
          <p class="no-posts-message">No recipes shared yet. Get ready for delicious dishes and cooking adventures!</p>
        {% endif %}
      </div>
    </div>
  </div>
</div>

<style>
.categories {
  .categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }
  
  .category-card {
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 2rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px var(--shadow-color);
    
    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 24px var(--shadow-color);
    }
    
    .category-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
      padding-bottom: 1rem;
      border-bottom: 2px solid var(--accent-color);
      
      .category-name {
        margin: 0;
        font-size: 1.25rem;
        
        .category-link {
          color: var(--text-color);
          text-decoration: none;
          
          &:hover {
            color: var(--accent-color);
          }
        }
      }
      
      .post-count {
        background-color: var(--accent-color);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
      }
    }
    
    .category-posts {
      .category-post {
        padding: 1rem 0;
        border-bottom: 1px solid var(--border-color);
        
        &:last-child {
          border-bottom: none;
          padding-bottom: 0;
        }
        
        .post-meta {
          margin-bottom: 0.5rem;
          
          time {
            font-size: 0.9rem;
            color: var(--text-muted);
          }
        }
        
        .post-title {
          margin-bottom: 0.5rem;
          font-size: 1rem;
          
          a {
            color: var(--text-color);
            text-decoration: none;
            
            &:hover {
              color: var(--accent-color);
            }
          }
        }
        
        .post-excerpt {
          color: var(--text-muted);
          font-size: 0.9rem;
          line-height: 1.5;
          margin: 0;
        }
      }
      
      .view-more {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border-color);
        
        .view-more-link {
          color: var(--accent-color);
          text-decoration: none;
          font-weight: 500;
          
          &:hover {
            text-decoration: underline;
          }
        }
      }
    }
  }
  
  .no-categories {
    text-align: center;
    padding: 3rem 2rem;
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    margin-top: 2rem;
    
    p {
      color: var(--text-muted);
      font-size: 1.1rem;
      margin: 0;
    }
  }
  
  .no-posts-message {
    color: var(--text-muted);
    font-style: italic;
    text-align: center;
    padding: 2rem 1rem;
    background-color: var(--hover-bg);
    border-radius: 8px;
    margin: 1rem 0;
    border: 1px solid var(--border-color);
  }
}

@media (max-width: 768px) {
  .categories .categories-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .categories .category-card {
    padding: 1.5rem;
  }
}
</style>
