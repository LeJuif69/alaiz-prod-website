// A LAIZ PROD - Script principal
document.addEventListener('DOMContentLoaded', function() {
    
    // Navigation mobile
    initMobileNavigation();
    
    // Navigation sticky
    initStickyNavigation();
    
    // Animations d'apparition
    initScrollAnimations();
    
    // Formulaires
    initForms();
    
    // Boutons WhatsApp
    initWhatsAppButtons();
    
    // Carrousels et sliders
    initSliders();
    
    // Filtres (pour le blog)
    initFilters();
});

/**
 * Navigation mobile (hamburger menu)
 */
function initMobileNavigation() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            // Fermer le menu en cliquant sur un lien
            const navLinks = navMenu.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    hamburger.classList.remove('active');
                    navMenu.classList.remove('active');
                });
            });
        });
        
        // Fermer le menu en cliquant en dehors
        document.addEventListener('click', (e) => {
            if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }
}

/**
 * Navigation sticky avec effet de transparence
 */
function initStickyNavigation() {
    const navbar = document.getElementById('navbar');
    
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
}

/**
 * Animations d'apparition au scroll
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.service-card, .stat-item, .article-card, .testimonial-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });
}

/**
 * Gestion des formulaires
 */
function initForms() {
    // Formulaire de contact
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
    
    // Formulaire newsletter
    const newsletterForms = document.querySelectorAll('.newsletter-form, .sidebar-newsletter-form');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', handleNewsletterForm);
    });
    
    // Validation en temps réel
    const formInputs = document.querySelectorAll('input[required], textarea[required], select[required]');
    formInputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
}

/**
 * Traitement du formulaire de contact
 */
async function handleContactForm(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Validation côté client
    if (!validateForm(form)) {
        return;
    }
    
    // État de chargement
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Envoi en cours...';
    submitBtn.disabled = true;
    
    try {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showNotification('Merci ! Votre demande a été envoyée. Nous vous répondrons sous 24h.', 'success');
            
            // Proposition WhatsApp
            if (result.whatsapp_url && confirm('Voulez-vous également envoyer votre demande via WhatsApp pour une réponse plus rapide ?')) {
                window.open(result.whatsapp_url, '_blank');
            }
            
            form.reset();
        } else {
            showNotification('Erreur : ' + result.message, 'error');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showNotification('Erreur lors de l\'envoi. Veuillez réessayer ou nous contacter directement.', 'error');
    } finally {
        // Restaurer le bouton
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

/**
 * Traitement du formulaire newsletter
 */
function handleNewsletterForm(e) {
    e.preventDefault();
    
    const form = e.target;
    const email = form.querySelector('input[type="email"]').value;
    
    if (!validateEmail(email)) {
        showNotification('Veuillez entrer une adresse email valide.', 'error');
        return;
    }
    
    // Simuler l'envoi (à remplacer par une vraie API)
    showNotification('Merci ! Vous êtes maintenant abonné à notre newsletter.', 'success');
    form.reset();
}

/**
 * Validation de formulaire
 */
function validateForm(form) {
    const requiredFields = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!validateField({ target: field })) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Validation d'un champ individuel
 */
function validateField(e) {
    const field = e.target;
    const value = field.value.trim();
    let isValid = true;
    let message = '';
    
    // Validation selon le type de champ
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'Ce champ est obligatoire';
    } else if (field.type === 'email' && value && !validateEmail(value)) {
        isValid = false;
        message = 'Email invalide';
    } else if (field.type === 'tel' && value && !validatePhone(value)) {
        isValid = false;
        message = 'Numéro de téléphone invalide';
    }
    
    // Affichage de l'erreur
    showFieldError(field, isValid ? '' : message);
    
    return isValid;
}

/**
 * Validation email
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validation téléphone
 */
function validatePhone(phone) {
    const re = /^[\+]?[0-9\s\-\(\)]{8,}$/;
    return re.test(phone);
}

/**
 * Affichage d'erreur sur un champ
 */
function showFieldError(field, message) {
    // Supprimer l'erreur existante
    clearFieldError({ target: field });
    
    if (message) {
        field.classList.add('error');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
    }
}

/**
 * Suppression d'erreur sur un champ
 */
function clearFieldError(e) {
    const field = e.target;
    field.classList.remove('error');
    
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

/**
 * Système de notifications
 */
function showNotification(message, type = 'info') {
    // Créer la notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Styles inline pour s'assurer qu'ils s'appliquent
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        background: type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6',
        color: 'white',
        padding: '1rem',
        borderRadius: '10px',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        zIndex: '9999',
        maxWidth: '400px',
        display: 'flex',
        alignItems: 'center',
        gap: '1rem'
    });
    
    // Ajouter au DOM
    document.body.appendChild(notification);
    
    // Fermeture automatique
    setTimeout(() => {
        notification.remove();
    }, 5000);
    
    // Fermeture manuelle
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.remove();
    });
}

/**
 * Boutons WhatsApp avec messages personnalisés
 */
function initWhatsAppButtons() {
    const whatsappButtons = document.querySelectorAll('[href*="wa.me"]');
    
    whatsappButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Analytics si disponible
            if (typeof gtag !== 'undefined') {
                gtag('event', 'click', {
                    'event_category': 'WhatsApp',
                    'event_label': this.textContent.trim()
                });
            }
        });
    });
}

/**
 * Carrousels et sliders simples
 */
function initSliders() {
    const sliders = document.querySelectorAll('.slider');
    
    sliders.forEach(slider => {
        const slides = slider.querySelectorAll('.slide');
        const prevBtn = slider.querySelector('.slider-prev');
        const nextBtn = slider.querySelector('.slider-next');
        let currentSlide = 0;
        
        if (slides.length === 0) return;
        
        function showSlide(index) {
            slides.forEach(slide => slide.style.display = 'none');
            slides[index].style.display = 'block';
        }
        
        function nextSlide() {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        }
        
        function prevSlide() {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            showSlide(currentSlide);
        }
        
        // Navigation
        if (nextBtn) nextBtn.addEventListener('click', nextSlide);
        if (prevBtn) prevBtn.addEventListener('click', prevSlide);
        
        // Auto-play
        setInterval(nextSlide, 5000);
        
        // Initialisation
        showSlide(0);
    });
}

/**
 * Système de filtres (pour le blog)
 */
function initFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const filterableItems = document.querySelectorAll('[data-category]');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.dataset.category;
            
            // Mise à jour des boutons actifs
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filtrage des éléments
            filterableItems.forEach(item => {
                if (category === 'all' || item.dataset.category === category) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Animation d'apparition
            setTimeout(() => {
                const visibleItems = Array.from(filterableItems).filter(item => 
                    item.style.display !== 'none'
                );
                visibleItems.forEach((item, index) => {
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                    }, index * 100);
                });
            }, 50);
        });
    });
}

/**
 * Smooth scroll pour les ancres
 */
function initSmoothScroll() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const navbarHeight = document.getElementById('navbar').offsetHeight;
                const targetPosition = targetElement.offsetTop - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Lazy loading des images
 */
function initLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
}

/**
 * Utilitaires divers
 */
const Utils = {
    // Debounce function
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },
    
    // Formatage des numéros de téléphone
    formatPhone: function(phone) {
        return phone.replace(/(\d{3})(\d{3})(\d{3})(\d{3})/, '+$1 $2 $3 $4');
    },
    
    // Génération d'URL WhatsApp
    generateWhatsAppUrl: function(phone, message) {
        const cleanPhone = phone.replace(/\D/g, '');
        const encodedMessage = encodeURIComponent(message);
        return `https://wa.me/${cleanPhone}?text=${encodedMessage}`;
    }
};

// Export pour utilisation dans d'autres scripts
window.ALaizProd = {
    Utils,
    showNotification,
    validateEmail,
    validatePhone
};
