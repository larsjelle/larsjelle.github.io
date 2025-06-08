---
title: Archives
icon: fas fa-archive
order: 3
layout: page
---

<div class="archives">
  <h2>All Posts</h2>
  
  {% if site.posts.size > 0 %}
    {% assign posts_by_year = site.posts | group_by_exp: 'post', 'post.date | date: "%Y"' %}
    
    {% for year_group in posts_by_year %}
      <div class="year-group">
        <h3 class="year-heading">{{ year_group.name }}</h3>
        
        <div class="posts-by-year">
          {% for post in year_group.items %}
            <article class="archive-post">
              <div class="post-date">
                <time datetime="{{ post.date | date_to_xmlschema }}">
                  {{ post.date | date: "%b %d" }}
                </time>
              </div>
              <div class="post-info">
                <h4 class="post-title">
                  <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                </h4>
                {% if post.categories.size > 0 %}
                  <div class="post-categories">
                    {% for category in post.categories %}
                      <span class="category">{{ category }}</span>
                    {% endfor %}
                  </div>
                {% endif %}
              </div>
            </article>
          {% endfor %}
        </div>
      </div>
    {% endfor %}
  {% else %}
    <div class="no-posts">
      <p>No posts available yet. Check back soon!</p>
    </div>
  {% endif %}
</div>

<style>
.archives {
  .year-group {
    margin-bottom: 3rem;
    
    .year-heading {
      font-size: 1.5rem;
      color: var(--accent-color);
      border-bottom: 2px solid var(--accent-color);
      padding-bottom: 0.5rem;
      margin-bottom: 1.5rem;
    }
  }
  
  .posts-by-year {
    .archive-post {
      display: flex;
      align-items: flex-start;
      gap: 1.5rem;
      padding: 1rem 0;
      border-bottom: 1px solid var(--border-color);
      
      &:last-child {
        border-bottom: none;
      }
      
      .post-date {
        flex-shrink: 0;
        width: 60px;
        
        time {
          font-size: 0.9rem;
          color: var(--text-muted);
          font-weight: 500;
        }
      }
      
      .post-info {
        flex: 1;
        
        .post-title {
          margin-bottom: 0.5rem;
          font-size: 1.1rem;
          
          a {
            color: var(--text-color);
            text-decoration: none;
            
            &:hover {
              color: var(--accent-color);
            }
          }
        }
        
        .post-categories {
          display: flex;
          gap: 0.5rem;
          flex-wrap: wrap;
          
          .category {
            background-color: var(--border-color);
            color: var(--text-muted);
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.8rem;
          }
        }
      }
    }
  }
  
  .no-posts {
    text-align: center;
    padding: 3rem 2rem;
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    
    p {
      color: var(--text-muted);
      font-size: 1.1rem;
      margin: 0;
    }
  }
}
</style>
