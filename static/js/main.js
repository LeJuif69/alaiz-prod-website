// A LAIZ PROD - JavaScript corrigé et fonctionnel
console.log('🚀 Initialisation A LAIZ PROD');

// Variables globales
let isAudioPlaying = false;
let aiChatActive = false;

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM chargé');
    
    // Masquer le loader rapidement
    setTimeout(() => {
        hideLoader();
        initializeWebsite();
    }, 1500);
});

function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.opacity = '0';
        loader.style.transition = 'opacity 0.5s ease';
        setTimeout(() => {
            loader.style.display = 'none';
        }, 500);
    }
}

function initializeWebsite() {
    console.log('Initialisation du site...');
    
    try {
        setupBasicInteractions();
        setupAIChat();
        setupFormHandlers();
        setupNavigation();
        loadWeatherData();
        showNotification('✅ Site A LAIZ PROD chargé !', 'success');
    } catch (error) {
        console.error('Erreur initialisation:', error);
        showNotification('⚠️ Certaines fonctionnalités peuvent être limitées', 'warning');
    }
}

// Configuration des interactions de base
function setupBasicInteractions() {
    // Curseur personnalisé
    const cursor = document.getElementById('cursor');
    if (cursor) {
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        });
    }

    // Animation des cartes au scroll
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
    });

    // Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    cards.forEach(card => observer.observe(card));
}

// Chat IA
function setupAIChat() {
    window.toggleAIChat = function() {
        const aiChat = document.getElementById('aiChat');
        if (!aiChat) return;
        
        aiChatActive = !aiChatActive;
        
        if (aiChatActive) {
            aiChat.style.display = 'flex';
            aiChat.classList.add('active');
            showNotification('🤖 Assistant IA activé', 'info');
        } else {
            aiChat.classList.remove('active');
            setTimeout(() => {
                aiChat.style.display = 'none';
            }, 300);
        }
    };

    window.handleChatInput = function(event) {
        if (event.key === 'Enter') {
            sendChatMessage();
        }
    };

    window.sendChatMessage = async function() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        addChatMessage(message, 'user');
        input.value = '';
        
        try {
            const response = await fetch('/api/ai-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            if (response.ok) {
                const data = await response.json();
                setTimeout(() => {
                    addChatMessage(data.response, 'bot');
                }, 1000);
            } else {
                throw new Error('Erreur serveur');
            }
        } catch (error) {
            console.error('Erreur chat:', error);
            setTimeout(() => {
                addChatMessage('Désolé, je ne peux pas répondre pour le moment.', 'bot');
            }, 1000);
        }
    };

    function addChatMessage(message, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ${sender}`;
        messageDiv.textContent = message;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// Gestion des formulaires
function setupFormHandlers() {
    const smartForm = document.getElementById('smartForm');
    if (!smartForm) return;
    
    smartForm.addEventListener('submit', handleFormSubmit);
    
    const projectDescription = document.getElementById('projectDescription');
    if (projectDescription) {
        projectDescription.addEventListener('input', debounce(analyzeProject, 2000));
    }
}

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        project: formData.get('project')
    };
    
    showNotification('📤 Envoi en cours...', 'info');
    
    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            const result = await response.json();
            showNotification('✅ Message envoyé avec succès !', 'success');
            event.target.reset();
            
            // Masquer les suggestions
            const suggestions = document.getElementById('aiSuggestions');
            if (suggestions) suggestions.style.display = 'none';
        } else {
            throw new Error('Erreur serveur');
        }
    } catch (error) {
        console.error('Erreur envoi:', error);
        showNotification('❌ Erreur lors de l\'envoi', 'error');
    }
}

async function analyzeProject() {
    const description = document.getElementById('projectDescription');
    const suggestions = document.getElementById('aiSuggestions');
    const suggestionsList = document.getElementById('suggestionsList');
    
    if (!description || !suggestions || description.value.length < 10) {
        if (suggestions) suggestions.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch('/api/smart-form', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ description: description.value })
        });
        
        if (response.ok) {
            const data = await response.json();
            
            if (data.suggestions && data.suggestions.length > 0) {
                suggestionsList.innerHTML = data.suggestions
                    .map(s => `<p style="margin: 0.5rem 0; color: var(--text-light);">${s}</p>`)
                    .join('');
                suggestions.style.display = 'block';
                showNotification('🤖 Suggestions IA générées', 'success');
            }
        }
    } catch (error) {
        console.error('Erreur analyse:', error);
    }
}

// Navigation
function setupNavigation() {
    window.addEventListener('scroll', () => {
        const navbar = document.getElementById('navbar');
        if (navbar) {
            if (window.pageYOffset > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    });
}

// Chargement météo
async function loadWeatherData() {
    try {
        const response = await fetch('/api/weather');
        if (response.ok) {
            const data = await response.json();
            
            const tempElement = document.getElementById('temperature');
            const conditionElement = document.getElementById('condition');
            const iconElement = document.querySelector('.weather-icon');
            
            if (tempElement) tempElement.textContent = data.temperature + '°C';
            if (conditionElement) conditionElement.textContent = data.condition;
            if (iconElement) iconElement.textContent = data.icon;
        }
    } catch (error) {
        console.log('Météo par défaut utilisée');
    }
}

// Audio player
function toggleAdvancedAudio() {
    const playIcon = document.getElementById('advancedPlayIcon');
    const progressBar = document.getElementById('audioProgress');
    
    if (!playIcon || !progressBar) return;
    
    if (!isAudioPlaying) {
        playIcon.className = 'fas fa-pause';
        isAudioPlaying = true;
        
        let progress = 0;
        const interval = setInterval(() => {
            progress += 2;
            progressBar.style.width = progress + '%';
            
            if (progress >= 100) {
                clearInterval(interval);
                playIcon.className = 'fas fa-play';
                isAudioPlaying = false;
                progressBar.style.width = '0%';
            }
        }, 200);
        
        showNotification('🎵 Lecture audio', 'info');
    } else {
        playIcon.className = 'fas fa-play';
        isAudioPlaying = false;
        progressBar.style.width = '0%';
    }
}

// Notifications
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    if (!notification) return;
    
    notification.textContent = message;
    notification.style.display = 'block';
    notification.style.opacity = '1';
    
    const colors = {
        'success': '#00ffff',
        'error': '#ff006e',
        'info': '#f39c12',
        'warning': '#ff9800'
    };
    
    notification.style.borderLeft = `4px solid ${colors[type]}`;
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.style.display = 'none';
        }, 300);
    }, 3000);
}

// Fonctions pour les boutons
function toggleTheme() {
    const body = document.body;
    const current = body.getAttribute('data-theme') || 'default';
    const themes = ['default', 'dark', 'neon'];
    const next = themes[(themes.indexOf(current) + 1) % themes.length];
    body.setAttribute('data-theme', next);
    showNotification(`🎨 Thème: ${next}`, 'info');
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
            showNotification('Plein écran non supporté', 'warning');
        });
    } else {
        document.exitFullscreen();
    }
}

function shareWebsite() {
    if (navigator.share) {
        navigator.share({
            title: 'A LAIZ PROD',
            text: 'Découvrez A LAIZ PROD',
            url: window.location.href
        }).catch(console.error);
    } else {
        navigator.clipboard.writeText(window.location.href).then(() => {
            showNotification('🔗 Lien copié !', 'success');
        }).catch(() => {
            showNotification('Impossible de copier le lien', 'warning');
        });
    }
}

function toggleMusicVisualizer() {
    showNotification('🎵 Visualiseur musical', 'info');
}

function toggleVoiceRecognition() {
    showNotification('🎤 Reconnaissance vocale bientôt disponible', 'info');
}

function openCalculator() {
    showNotification('🧮 Calculateur de devis en développement', 'info');
}

function scheduleVR() {
    showNotification('🥽 Démo VR bientôt disponible', 'info');
}

// Fonction utilitaire
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Raccourcis clavier
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey) {
        switch(e.key) {
            case '1':
                window.location.href = '/';
                e.preventDefault();
                break;
            case '2':
                window.location.href = '/services';
                e.preventDefault();
                break;
            case '3':
                window.location.href = '/contact';
                e.preventDefault();
                break;
            case 'i':
                toggleAIChat();
                e.preventDefault();
                break;
        }
    }
    
    if (e.key === 'Escape' && aiChatActive) {
        toggleAIChat();
    }
});

// Gestion des erreurs globales
window.addEventListener('error', (e) => {
    console.error('Erreur JavaScript:', e.error);
});

// Export global
window.AlaizProd = {
    toggleAIChat: toggleAIChat,
    showNotification: showNotification,
    toggleTheme: toggleTheme,
    toggleFullscreen: toggleFullscreen,
    shareWebsite: shareWebsite
};

console.log('✅ A LAIZ PROD JavaScript chargé avec succès !');