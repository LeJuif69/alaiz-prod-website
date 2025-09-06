// A LAIZ PROD - JavaScript Principal
// =================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation
    initializeApp();
});

function initializeApp() {
    // Loading screen
    handleLoadingScreen();
    
    // Navigation
    initializeNavigation();
    
    // Animations
    initializeAnimations();
    
    // Forms
    initializeForms();
    
    // Stats counters
    initializeStatsCounters();
    
    // Flash messages
    handleFlashMessages();
    
    // Smooth scrolling
    initializeSmoothScrolling();
    
    // Mobile menu
    initializeMobileMenu();
}

// =================================
// LOADING SCREEN
// =================================
function handleLoadingScreen() {
    window.addEventListener('load', function() {
        const loading = document.getElementById('loading');
        if (loading) {
            setTimeout(() => {
                loading.style.opacity = '0';
                setTimeout(() => {
                    loading.style.display = 'none';
                }, 500);
            }, 1000);
        }
    });
}

// =================================
// NAVIGATION
// =================================
function initializeNavigation() {
    // Navbar background on scroll
    window.addEventListener('scroll', function() {
        const navbar = document.getElementById('navbar');
        if (navbar) {
            if (window.scrollY > 100) {
                navbar.style.background = 'rgba(45, 55, 72, 0.98)';
                navbar.style.borderBottom = '1px solid rgba(255, 255, 255, 0.2)';
            } else {
                navbar.style.background = 'rgba(45, 55, 72, 0.95)';
                navbar.style.borderBottom = '1px solid rgba(255, 255, 255, 0.1)';
            }
        }
    });
    
    // Active nav link highlighting
    highlightActiveNavLink();
}

function highlightActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath) {
            link.style.color = 'var(--secondary-color)';
            link.style.fontWeight = '600';
        }
    });
}

// =================================
// MOBILE MENU
// =================================
function initializeMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
            
            // Animation des barres du hamburger
            const spans = mobileMenuBtn.querySelectorAll('span');
            if (mobileMenuBtn.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        // Fermer le menu mobile quand on clique sur un lien
        navLinks.addEventListener('click', function() {
            navLinks.classList.remove('active');
            mobileMenuBtn.classList.remove('active');
            
            const spans = mobileMenuBtn.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        });
    }
}

// =================================
// SMOOTH SCROLLING
// =================================
function initializeSmoothScrolling() {
    // Smooth scroll pour les ancres internes
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            
            if (target) {
                const navbarHeight = document.getElementById('navbar').offsetHeight;
                const targetPosition = target.offsetTop - navbarHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// =================================
// ANIMATIONS
// =================================
function initializeAnimations() {
    // Observer pour les animations au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                
                // Animation spéciale pour les cartes
                if (entry.target.classList.contains('service-card') || 
                    entry.target.classList.contains('testimonial-card') ||
                    entry.target.classList.contains('pricing-card')) {
                    // Délai pour effet cascade
                    const cards = entry.target.parentElement.children;
                    const index = Array.from(cards).indexOf(entry.target);
                    entry.target.style.animationDelay = `${index * 0.1}s`;
                }
            }
        });
    }, observerOptions);

    // Observer tous les éléments avec la classe animate-on-scroll
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
    
    // Parallax léger pour les héros
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero-background');
        
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
}

// =================================
// STATISTIQUES ANIMÉES
// =================================
function initializeStatsCounters() {
    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counters = entry.target.querySelectorAll('.stat-number');
                
                counters.forEach((counter) => {
                    const target = parseInt(counter.getAttribute('data-target'));
                    animateCounter(counter, target, 2000);
                });
                
                // Ne déclencher qu'une fois
                statsObserver.unobserve(entry.target);
            }
        });
    });

    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
}

function animateCounter(element, target, duration) {
    let start = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target + '+';
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start) + '+';
        }
    }, 16);
}

// =================================
// FORMULAIRES
// =================================
function initializeForms() {
    // Validation en temps réel
    setupFormValidation();
    
    // Auto-formatage des champs
    setupAutoFormatting();
    
    // Soumission des formulaires
    setupFormSubmission();
}

function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        
        inputs.forEach(input => {
            // Validation en temps réel
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('error')) {
                    validateField(this);
                }
            });
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    let isValid = true;
    let errorMessage = '';
    
    // Validation selon le type de champ
    switch(fieldType) {
        case 'email':
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            isValid = emailRegex.test(value);
            errorMessage = 'Email invalide';
            break;
            
        case 'tel':
            const phoneRegex = /^\+237[0-9]{8,9}$/;
            isValid = phoneRegex.test(value.replace(/\s/g, ''));
            errorMessage = 'Numéro de téléphone invalide (+237XXXXXXXX)';
            break;
            
        case 'text':
            if (field.name === 'name') {
                isValid = value.length >= 2;
                errorMessage = 'Le nom doit contenir au moins 2 caractères';
            }
            break;
            
        default:
            isValid = value.length > 0;
            errorMessage = 'Ce champ est requis';
    }
    
    // Application du style d'erreur
    if (isValid) {
        field.classList.remove('error');
        removeFieldError(field);
    } else {
        field.classList.add('error');
        showFieldError(field, errorMessage);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    removeFieldError(field); // Supprimer l'erreur existante
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = 'var(--error-color)';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
    
    field.parentNode.appendChild(errorDiv);
    field.style.borderColor = 'var(--error-color)';
}

function removeFieldError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    field.style.borderColor = '';
}

function setupAutoFormatting() {
    // Formatage automatique du téléphone
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            // Ajouter automatiquement +237 pour les numéros camerounais
            if (value.length > 0 && !value.startsWith('237')) {
                if (value.startsWith('6') || value.startsWith('2')) {
                    value = '237' + value;
                }
            }
            
            if (value.startsWith('237')) {
                value = '+' + value;
            }
            
            e.target.value = value;
        });
    });
    
    // Formatage automatique du nom (première lettre en majuscule)
    const nameInputs = document.querySelectorAll('input[name="name"]');
    nameInputs.forEach(input => {
        input.addEventListener('blur', function(e) {
            const words = e.target.value.toLowerCase().split(' ');
            const formattedWords = words.map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
            );
            e.target.value = formattedWords.join(' ');
        });
    });
}

function setupFormSubmission() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            const requiredFields = form.querySelectorAll('input[required], textarea[required]');
            let isFormValid = true;
            
            // Validation de tous les champs requis
            requiredFields.forEach(field => {
                if (!validateField(field)) {
                    isFormValid = false;
                }
            });
            
            if (!isFormValid) {
                e.preventDefault();
                showNotification('Veuillez corriger les erreurs dans le formulaire', 'error');
                return;
            }
            
            // État de chargement du bouton
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Envoi en cours...';
                submitBtn.disabled = true;
                
                // Restaurer le bouton après 5 secondes (au cas où)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
}

// =================================
// FAQ
// =================================
function toggleFAQ(element) {
    const faqItem = element.parentNode;
    const answer = faqItem.querySelector('.faq-answer');
    const icon = element.querySelector('i');
    
    // Fermer toutes les autres FAQ
    document.querySelectorAll('.faq-item.active').forEach(item => {
        if (item !== faqItem) {
            item.classList.remove('active');
            item.querySelector('.faq-answer').style.maxHeight = '0px';
            item.querySelector('.faq-question i').style.transform = 'rotate(0deg)';
        }
    });
    
    // Toggle la FAQ actuelle
    faqItem.classList.toggle('active');
    
    if (faqItem.classList.contains('active')) {
        answer.style.maxHeight = answer.scrollHeight + 'px';
        icon.style.transform = 'rotate(180deg)';
    } else {
        answer.style.maxHeight = '0px';
        icon.style.transform = 'rotate(0deg)';
    }
}

// =================================
// FLASH MESSAGES
// =================================
function handleFlashMessages() {
    // Auto-masquer les flash messages après 5 secondes
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        setTimeout(() => {
            flashMessages.style.opacity = '0';
            setTimeout(() => flashMessages.remove(), 500);
        }, 5000);
    }
}

// =================================
// NOTIFICATIONS
// =================================
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="background: none; border: none; color: inherit; font-size: 1.2rem; cursor: pointer; margin-left: 1rem;">×</button>
    `;
    
    document.body.appendChild(notification);
    
    // Animation d'entrée
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto-suppression
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// =================================
// LAZY LOADING DES IMAGES
// =================================
function initializeLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
}

// =================================
// UTILITAIRES
// =================================

// Debounce function pour optimiser les performances
function debounce(func, wait, immediate) {
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
}

// Throttle function pour les événements de scroll
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Optimisation des événements de scroll avec throttle
window.addEventListener('scroll', throttle(function() {
    // Code optimisé pour le scroll
    const scrolled = window.pageYOffset;
    
    // Parallax pour le hero
    const hero = document.querySelector('.hero-background');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.3}px)`;
    }
    
    // Bouton "retour en haut" (si ajouté)
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        if (scrolled > 500) {
            backToTop.style.opacity = '1';
            backToTop.style.visibility = 'visible';
        } else {
            backToTop.style.opacity = '0';
            backToTop.style.visibility = 'hidden';
        }
    }
}, 16));

// =================================
// ANALYTICS & TRACKING
// =================================
function trackEvent(action, category, label) {
    // Google Analytics tracking (si configuré)
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            'event_category': category,
            'event_label': label
        });
    }
    
    console.log(`Event tracked: ${action} - ${category} - ${label}`);
}

// Track des clics sur les boutons CTA
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-primary')) {
        const buttonText = e.target.textContent.trim();
        trackEvent('click', 'CTA Button', buttonText);
    }
    
    if (e.target.closest('a[href^="tel:"]')) {
        trackEvent('click', 'Phone Call', 'Phone Click');
    }
    
    if (e.target.closest('a[href^="mailto:"]')) {
        trackEvent('click', 'Email', 'Email Click');
    }
    
    if (e.target.closest('a[href*="wa.me"]')) {
        trackEvent('click', 'WhatsApp', 'WhatsApp Click');
    }
});

// =================================
// EXPORTS POUR UTILISATION GLOBALE
// =================================
window.AlaizProd = {
    showNotification,
    toggleFAQ,
    trackEvent
};

console.log('🎵 A Laiz Prod - Site chargé avec succès!');

/**
 * PORTFOLIO AUDIO - A LAIZ PROD
 */

// Classe pour gérer le portfolio audio
class AudioPortfolio {
    constructor() {
        this.currentAudio = null;
        this.currentButton = null;
        this.audioFiles = {
            'jazz-standards': '/static/audio/jazz-standards.mp3',
            'wedding-music': '/static/audio/wedding-music.mp3',
            'live-concert': '/static/audio/live-concert.mp3',
            'afro-rhythms': '/static/audio/afro-rhythms.mp3'
        };
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        document.querySelectorAll('.play-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handlePlayPause(e));
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.audio-card')) {
                this.stopAllAudio();
            }
        });
    }

    handlePlayPause(event) {
        const button = event.currentTarget;
        const audioType = button.getAttribute('data-audio');
        const icon = button.querySelector('i');
        const audioWave = button.closest('.audio-player').querySelector('.audio-wave');
        
        if (button === this.currentButton && this.currentAudio && !this.currentAudio.paused) {
            this.pauseAudio(button, icon, audioWave);
            return;
        }

        this.stopAllAudio();
        this.playAudio(audioType, button, icon, audioWave);
    }

    playAudio(audioType, button, icon, audioWave) {
        try {
            this.currentAudio = new Audio(this.audioFiles[audioType]);
            this.currentButton = button;

            this.currentAudio.volume = 0.7;
            this.currentAudio.loop = false;

            this.currentAudio.addEventListener('loadstart', () => {
                this.updateUI(button, icon, audioWave, 'loading');
            });

            this.currentAudio.addEventListener('canplay', () => {
                this.updateUI(button, icon, audioWave, 'playing');
                this.currentAudio.play();
            });

            this.currentAudio.addEventListener('ended', () => {
                this.updateUI(button, icon, audioWave, 'stopped');
                this.resetCurrentAudio();
            });

            this.currentAudio.addEventListener('error', (e) => {
                console.warn(`Erreur audio pour ${audioType}:`, e);
                this.showAudioError(button);
                this.resetCurrentAudio();
            });

            this.currentAudio.load();

        } catch (error) {
            console.warn('Erreur lors de la lecture audio:', error);
            this.showAudioError(button);
        }
    }

    pauseAudio(button, icon, audioWave) {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.updateUI(button, icon, audioWave, 'paused');
        }
    }

    stopAllAudio() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
        }

        document.querySelectorAll('.play-btn').forEach(btn => {
            const icon = btn.querySelector('i');
            const audioWave = btn.closest('.audio-player').querySelector('.audio-wave');
            this.updateUI(btn, icon, audioWave, 'stopped');
        });

        this.resetCurrentAudio();
    }

    updateUI(button, icon, audioWave, state) {
        button.classList.remove('playing', 'loading');
        audioWave.classList.remove('playing');
        
        switch (state) {
            case 'loading':
                icon.className = 'fas fa-spinner fa-spin';
                break;
            case 'playing':
                icon.className = 'fas fa-pause';
                button.classList.add('playing');
                audioWave.classList.add('playing');
                break;
            case 'paused':
            case 'stopped':
            default:
                icon.className = 'fas fa-play';
                break;
        }
    }

    showAudioError(button) {
        const icon = button.querySelector('i');
        icon.className = 'fas fa-exclamation-triangle';
        
        setTimeout(() => {
            icon.className = 'fas fa-play';
        }, 2000);
    }

    resetCurrentAudio() {
        this.currentAudio = null;
        this.currentButton = null;
    }
}

// Initialisation du portfolio audio
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.portfolio-audio')) {
        new AudioPortfolio();
    }
});
