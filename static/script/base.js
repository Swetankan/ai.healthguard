  document.addEventListener('DOMContentLoaded', () => {
    const navbarLinks = document.querySelectorAll('.nav_bar_text a');

    navbarLinks.forEach(link => {
      link.addEventListener('click', function() {
        navbarLinks.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
      });
    });

    // Automatically set the active class based on the current URL
    const currentPath = window.location.pathname;
    navbarLinks.forEach(link => {
      if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
      }
    });
    
  });
