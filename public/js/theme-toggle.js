// Theme toggle functionality
document.addEventListener('DOMContentLoaded', function() {
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const themeToggleSidebar = document.getElementById('theme-toggle-btn-sidebar');
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  const body = document.body;
  
  console.log('Theme toggle script loaded');
  console.log('Theme toggle button found:', !!themeToggleBtn);
  console.log('Theme toggle sidebar button found:', !!themeToggleSidebar);
  
  // Load saved theme or detect system preference
  function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      body.setAttribute('data-theme', savedTheme);
      console.log('Loaded saved theme:', savedTheme);
    } else {
      // Auto-detect system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const initialTheme = prefersDark ? 'dark' : 'light';
      body.setAttribute('data-theme', initialTheme);
      console.log('Set initial theme:', initialTheme);
    }
  }
  
  // Theme toggle function
  function toggleTheme() {
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    console.log('Theme changed from', currentTheme, 'to', newTheme);
  }
  
  // Initialize theme first
  loadTheme();
  
  // Theme toggle for topbar button
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', toggleTheme);
  } else {
    console.error('Theme toggle button not found!');
  }
  
  // Theme toggle for sidebar button
  if (themeToggleSidebar) {
    themeToggleSidebar.addEventListener('click', toggleTheme);
  }
  
  // Sidebar toggle for mobile
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function() {
      sidebar.classList.toggle('active');
    });
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
      if (window.innerWidth <= 768) {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
          sidebar.classList.remove('active');
        }
      }
    });
  }

  // Listen for system theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (!localStorage.getItem('theme')) {
      const newTheme = e.matches ? 'dark' : 'light';
      body.setAttribute('data-theme', newTheme);
      console.log('System theme changed to:', newTheme);
    }
  });
  
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // Back to top functionality
  const backToTop = document.createElement('button');
  backToTop.innerHTML = '<i class="fas fa-chevron-up"></i>';
  backToTop.className = 'back-to-top';
  backToTop.setAttribute('aria-label', 'Back to top');
  document.body.appendChild(backToTop);
  
  window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
      backToTop.classList.add('visible');
    } else {
      backToTop.classList.remove('visible');
    }
  });
  
  backToTop.addEventListener('click', function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
});
