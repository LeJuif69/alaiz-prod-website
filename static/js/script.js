// A Laiz Prod - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    console.log('A Laiz Prod website loaded');
    
    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navList = document.querySelector('.nav-list');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            this.classList.toggle('active');
            navList.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-list a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navList.classList.remove('active');
        });
    });
    
    // Header scroll effect
    const header = document.querySelector('.header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            header.style.background = 'rgba(10, 10, 10, 0.95)';
            header.style.padding = '0.7rem 0';
        } else {
            header.style.background = 'rgba(10, 10, 10, 0.9)';
            header.style.padding = '1rem 0';
        }
    });
    
    // Animated counters
    const counters = document.querySelectorAll('.stat-number');
    const speed = 200;
    
    function animateCounters() {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-count');
            const count = +counter.innerText;
            const increment = Math.ceil(target / speed);
            
            if (count < target) {
                counter.innerText = Math.min(count + increment, target);
                setTimeout(() => animateCounters(), 1);
            }
        });
    }
    
    // Initialize counters when they come into view
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    const statsSection = document.querySelector('.stats');
    if (statsSection) {
        observer.observe(statsSection);
    }
    
    // Portfolio filtering
    const filterButtons = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Get filter value
            const filterValue = this.getAttribute('data-filter');
            
            // Filter portfolio items
            portfolioItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
    
    // Contact form validation
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Basic validation
            const nameInput = this.querySelector('input[type="text"]');
            const emailInput = this.querySelector('input[type="email"]');
            const messageInput = this.querySelector('textarea');
            
            let isValid = true;
            
            if (!nameInput.value.trim()) {
                isValid = false;
                highlightError(nameInput);
            } else {
                removeHighlight(nameInput);
            }
            
            if (!emailInput.value.trim() || !isValidEmail(emailInput.value)) {
                isValid = false;
                highlightError(emailInput);
            } else {
                removeHighlight(emailInput);
            }
            
            if (!messageInput.value.trim()) {
                isValid = false;
                highlightError(messageInput);
            } else {
                removeHighlight(messageInput);
            }
            
            if (isValid) {
                // Form is valid, you can submit it here
                alert('Merci pour votre message! Nous vous contacterons bientôt.');
                this.reset();
            }
        });
    }
    
    function highlightError(element) {
        element.style.borderColor = 'red';
    }
    
    function removeHighlight(element) {
        element.style.borderColor = '#ddd';
    }
    
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    console.log('JavaScript functionality initialized');
});
