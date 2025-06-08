---
title: Tags
icon: fas fa-tags
order: 2
layout: page
---

<div class="tags">
  <h2>Post Tags</h2>
  
  {% assign tags = site.tags | sort %}
  {% if tags.size > 0 %}
    <div class="tags-cloud">
      {% for tag in tags %}
        {% assign tag_name = tag[0] %}
        {% assign posts = tag[1] %}
        {% assign post_count = posts.size %}
        
        <a href="#{{ tag_name | slugify }}" class="tag-item" data-count="{{ post_count }}">
          <span class="tag-name">#{{ tag_name }}</span>
          <span class="tag-count">{{ post_count }}</span>
        </a>
      {% endfor %}
    </div>
    
    <div class="tags-content">
      {% for tag in tags %}
        {% assign tag_name = tag[0] %}
        {% assign posts = tag[1] %}
        
        <div class="tag-section" id="{{ tag_name | slugify }}">
          <div class="tag-header">
            <h3 class="tag-title">#{{ tag_name }}</h3>
            <span class="posts-count">{{ posts.size }} post{% if posts.size != 1 %}s{% endif %}</span>
          </div>
          
          <div class="tag-posts">
            {% for post in posts %}
              <article class="tag-post">
                <div class="post-info">
                  <h4 class="post-title">
                    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                  </h4>
                  <div class="post-meta">
                    <time datetime="{{ post.date | date_to_xmlschema }}">
                      {{ post.date | date: "%B %d, %Y" }}
                    </time>
                    {% if post.categories.size > 0 %}
                      <span class="post-categories">
                        {% for category in post.categories %}
                          <span class="category">{{ category }}</span>
                        {% endfor %}
                      </span>
                    {% endif %}
                  </div>
                  {% if post.excerpt %}
                    <p class="post-excerpt">{{ post.excerpt | strip_html | truncate: 150 }}</p>
                  {% endif %}
                </div>
              </article>
            {% endfor %}
          </div>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <div class="no-tags">
      <p>No tags available yet. Posts will be tagged and organized here once they're published!</p>
    </div>
  {% endif %}
</div>

<style>
.tags {
  .tags-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 3rem;
    padding: 2rem;
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    box-shadow: 0 2px 8px var(--shadow-color);
    
    .tag-item {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem 1rem;
      background-color: var(--border-color);
      color: var(--text-color);
      text-decoration: none;
      border-radius: 25px;
      transition: all 0.3s ease;
      border: 1px solid transparent;
      
      &:hover {
        background-color: var(--accent-color);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px var(--shadow-color);
      }
      
      .tag-name {
        font-weight: 500;
      }
      
      .tag-count {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        min-width: 20px;
        text-align: center;
      }
      
      // Size variations based on post count
      &[data-count="1"] {
        font-size: 0.85rem;
      }
      
      &[data-count="2"], &[data-count="3"] {
        font-size: 0.9rem;
      }
      
      &[data-count="4"], &[data-count="5"] {
        font-size: 1rem;
      }
      
      &[data-count^="6"], &[data-count^="7"], &[data-count^="8"], &[data-count^="9"] {
        font-size: 1.1rem;
        font-weight: 600;
      }
    }
  }
  
  .tags-content {
    .tag-section {
      margin-bottom: 3rem;
      background-color: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 2rem;
      box-shadow: 0 2px 8px var(--shadow-color);
      
      .tag-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--accent-color);
        
        .tag-title {
          margin: 0;
          color: var(--accent-color);
          font-size: 1.5rem;
        }
        
        .posts-count {
          background-color: var(--accent-color);
          color: white;
          padding: 0.3rem 0.8rem;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 500;
        }
      }
      
      .tag-posts {
        .tag-post {
          padding: 1.5rem 0;
          border-bottom: 1px solid var(--border-color);
          
          &:last-child {
            border-bottom: none;
            padding-bottom: 0;
          }
          
          .post-info {
            .post-title {
              margin-bottom: 0.75rem;
              font-size: 1.1rem;
              
              a {
                color: var(--text-color);
                text-decoration: none;
                
                &:hover {
                  color: var(--accent-color);
                }
              }
            }
            
            .post-meta {
              display: flex;
              align-items: center;
              gap: 1rem;
              margin-bottom: 0.75rem;
              font-size: 0.9rem;
              color: var(--text-muted);
              
              .post-categories {
                display: flex;
                gap: 0.5rem;
                
                .category {
                  background-color: var(--border-color);
                  color: var(--text-muted);
                  padding: 0.2rem 0.6rem;
                  border-radius: 12px;
                  font-size: 0.8rem;
                }
              }
            }
            
            .post-excerpt {
              color: var(--text-muted);
              line-height: 1.6;
              margin: 0;
            }
          }
        }
      }
    }
  }
  
  .no-tags {
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
}

@media (max-width: 768px) {
  .tags {
    .tags-cloud {
      padding: 1.5rem;
      gap: 0.5rem;
      
      .tag-item {
        padding: 0.4rem 0.8rem;
        font-size: 0.85rem !important;
      }
    }
    
    .tags-content .tag-section {
      padding: 1.5rem;
      
      .tag-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
        
        .tag-title {
          font-size: 1.25rem;
        }
      }
      
      .tag-posts .tag-post .post-info .post-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
      }
    }
  }
}
</style>
