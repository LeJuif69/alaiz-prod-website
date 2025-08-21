import os
import smtplib
import gzip
import json
import sqlite3
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, jsonify, request, session, make_response, render_template_string
from flask_babel import Babel, _, get_locale, ngettext
from datetime import datetime, timedelta
from urllib.parse import urljoin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
import requests
import stripe
import openai
from typing import Optional

app = Flask(__name__)

# Configuration de base
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configuration multi-langues
app.config['LANGUAGES'] = {
    'fr': 'Français',
    'en': 'English', 
    'es': 'Español'
}
app.config['BABEL_DEFAULT_LOCALE'] = 'fr'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

# Configuration SEO
app.config['GOOGLE_ANALYTICS_ID'] = os.environ.get('GOOGLE_ANALYTICS_ID', '')
app.config['SITE_URL'] = os.environ.get('SITE_URL', 'https://alaizopays.art')

# Configuration Email
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': os.environ.get('SMTP_EMAIL', 'contact@alaizopays.art'),
    'password': os.environ.get('SMTP_PASSWORD', 'Flavie190992'),
    'admin_email': os.environ.get('ADMIN_EMAIL', 'contact@alaizopays.art')
}

# Configuration IA
AI_CONFIG = {
    'openai_api_key': os.environ.get('OPENAI_API_KEY', ''),
    'claude_api_key': os.environ.get('CLAUDE_API_KEY', ''),
    'default_model': 'gpt-3.5-turbo',
    'max_tokens': 150,
    'temperature': 0.7
}

# Configuration Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_...')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', 'pk_test_...')

# Middleware pour proxy (nécessaire pour HTTPS sur Render)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Initialiser Babel
babel = Babel()
babel.init_app(app)

# Dictionnaires de traductions
TRANSLATIONS = {
    'fr': {
        'Accueil': 'Accueil',
        'Services': 'Services',
        'Label': 'Label',
        'Artiste': 'Artiste',
        'Boutique': 'Boutique',
        'Contact': 'Contact',
        'Formations': 'Formations',
        'À Propos': 'À Propos',
        'Changer de thème': 'Changer de thème',
        'Plein écran': 'Plein écran',
        'Partager': 'Partager',
        'Visualiseur musical': 'Visualiseur musical',
        'Yaoundé': 'Yaoundé',
        'Partiellement nuageux': 'Partiellement nuageux',
        'Reconnaissance vocale': 'Reconnaissance vocale',
        'Assistant LAIZ IA': 'Assistant LAIZ IA',
        'Fermer le chat': 'Fermer le chat',
        'Bonjour ! Je suis l\'assistant IA d\'A LAIZ PROD. Comment puis-je vous aider aujourd\'hui ?': 'Bonjour ! Je suis l\'assistant IA d\'A LAIZ PROD. Comment puis-je vous aider aujourd\'hui ?',
        'Tapez votre message...': 'Tapez votre message...',
        'Envoyer le message': 'Envoyer le message',
        'Appuyez sur Entrée pour envoyer votre message': 'Appuyez sur Entrée pour envoyer votre message',
        'Métriques de performance': 'Métriques de performance',
        'Latence': 'Latence',
        'L\'Art qui élève, la musique qui relie, la technologie qui transforme.': 'L\'Art qui élève, la musique qui relie, la technologie qui transforme.',
        'Tous droits réservés': 'Tous droits réservés',
        'Présence internationale': 'Présence internationale',
        'Technologie du futur': 'Technologie du futur',
        'hero_title': 'A LAIZ PROD',
        'hero_slogan': 'L\'Art qui élève, la musique qui relie.',
        'hero_description': 'Des prestations artistiques et pédagogiques d\'exception, signées Hervé & Flavie Nanfang. Une approche révolutionnaire qui fusionne tradition africaine et innovation technologique.',
        'reserve_prestation': 'Réserver une prestation',
        'explorer_formations': 'Explorer les formations',
        'assistant_ia': 'Assistant IA',
        'notre_univers': 'Notre Univers Artistique',
        'seo_description': 'A LAIZ PROD révolutionne l\'art musical avec des technologies immersives. Prestations artistiques premium, formations IA-assistées et productions musicales innovantes au Cameroun.',
        'seo_keywords': 'musique, formation musicale, IA, réalité virtuelle, Cameroun, Hervé Nanfang, piano, concert, mariage, événement, Yaoundé'
    },
    'en': {
        'Accueil': 'Home',
        'Services': 'Services',
        'Label': 'Label',
        'Artiste': 'Artist',
        'Boutique': 'Shop',
        'Contact': 'Contact',
        'Formations': 'Training',
        'À Propos': 'About',
        'Changer de thème': 'Change theme',
        'Plein écran': 'Fullscreen',
        'Partager': 'Share',
        'Visualiseur musical': 'Music visualizer',
        'Yaoundé': 'Yaoundé',
        'Partiellement nuageux': 'Partly cloudy',
        'Reconnaissance vocale': 'Voice recognition',
        'Assistant LAIZ IA': 'LAIZ AI Assistant',
        'Fermer le chat': 'Close chat',
        'Bonjour ! Je suis l\'assistant IA d\'A LAIZ PROD. Comment puis-je vous aider aujourd\'hui ?': 'Hello! I\'m A LAIZ PROD\'s AI assistant. How can I help you today?',
        'Tapez votre message...': 'Type your message...',
        'Envoyer le message': 'Send message',
        'Appuyez sur Entrée pour envoyer votre message': 'Press Enter to send your message',
        'Métriques de performance': 'Performance metrics',
        'Latence': 'Latency',
        'L\'Art qui élève, la musique qui relie, la technologie qui transforme.': 'Art that elevates, music that connects, technology that transforms.',
        'Tous droits réservés': 'All rights reserved',
        'Présence internationale': 'International presence',
        'Technologie du futur': 'Future technology',
        'hero_title': 'A LAIZ PROD',
        'hero_slogan': 'Art that elevates, music that connects.',
        'hero_description': 'Exceptional artistic and educational performances by Hervé & Flavie Nanfang. A revolutionary approach that fuses African tradition with technological innovation.',
        'reserve_prestation': 'Book a performance',
        'explorer_formations': 'Explore training',
        'assistant_ia': 'AI Assistant',
        'notre_univers': 'Our Artistic Universe',
        'seo_description': 'A LAIZ PROD revolutionizes musical art with immersive technologies. Premium artistic performances, AI-assisted training and innovative musical productions in Cameroon.',
        'seo_keywords': 'music, musical training, AI, virtual reality, Cameroon, Hervé Nanfang, piano, concert, wedding, event, Yaoundé'
    },
    'es': {
        'Accueil': 'Inicio',
        'Services': 'Servicios',
        'Label': 'Sello',
        'Artiste': 'Artista',
        'Boutique': 'Tienda',
        'Contact': 'Contacto',
        'Formations': 'Formación',
        'À Propos': 'Acerca de',
        'Changer de thème': 'Cambiar tema',
        'Plein écran': 'Pantalla completa',
        'Partager': 'Compartir',
        'Visualiseur musical': 'Visualizador musical',
        'Yaoundé': 'Yaundé',
        'Partiellement nuageux': 'Parcialmente nublado',
        'Reconnaissance vocale': 'Reconocimiento de voz',
        'Assistant LAIZ IA': 'Asistente IA LAIZ',
        'Fermer le chat': 'Cerrar chat',
        'Bonjour ! Je suis l\'assistant IA d\'A LAIZ PROD. Comment puis-je vous aider aujourd\'hui ?': '¡Hola! Soy el asistente IA de A LAIZ PROD. ¿Cómo puedo ayudarte hoy?',
        'Tapez votre message...': 'Escribe tu mensaje...',
        'Envoyer le message': 'Enviar mensaje',
        'Appuyez sur Entrée pour envoyer votre message': 'Presiona Enter para enviar tu mensaje',
        'Métriques de performance': 'Métricas de rendimiento',
        'Latence': 'Latencia',
        'L\'Art qui élève, la musique qui relie, la technologie qui transforme.': 'Arte que eleva, música que conecta, tecnología que transforma.',
        'Tous droits réservés': 'Todos los derechos reservados',
        'Présence internationale': 'Presencia internacional',
        'Technologie du futur': 'Tecnología del futuro',
        'hero_title': 'A LAIZ PROD',
        'hero_slogan': 'Arte que eleva, música que conecta.',
        'hero_description': 'Actuaciones artísticas y educativas excepcionales de Hervé & Flavie Nanfang. Un enfoque revolucionario que fusiona la tradición africana con la innovación tecnológica.',
        'reserve_prestation': 'Reservar actuación',
        'explorer_formations': 'Explorar formación',
        'assistant_ia': 'Asistente IA',
        'notre_univers': 'Nuestro Universo Artístico',
        'seo_description': 'A LAIZ PROD revoluciona el arte musical con tecnologías inmersivas. Actuaciones artísticas premium, formación asistida por IA y producciones musicales innovadoras en Camerún.',
        'seo_keywords': 'música, formación musical, IA, realidad virtual, Camerún, Hervé Nanfang, piano, concierto, boda, evento, Yaundé'
    }
}

@babel.localeselector
def get_locale():
    # 1. Check URL parameter
    requested_lang = request.args.get('lang')
    if requested_lang in app.config['LANGUAGES']:
        session['language'] = requested_lang
        return requested_lang
    
    # 2. Check session
    if 'language' in session and session['language'] in app.config['LANGUAGES']:
        return session['language']
    
    # 3. Check Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'fr'

def get_translation(key, lang=None):
    """Récupère une traduction"""
    if lang is None:
        lang = get_locale()
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['fr'].get(key, key))

# Template helper function
@app.template_global()
def _(key):
    return get_translation(key)

# SEO helpers
@app.template_global()
def get_seo_data(page='accueil'):
    """Génère les données SEO pour une page"""
    lang = get_locale()
    
    seo_data = {
        'accueil': {
            'title': f"A LAIZ PROD | {get_translation('hero_slogan', lang)}",
            'description': get_translation('seo_description', lang),
            'keywords': get_translation('seo_keywords', lang),
            'og_type': 'website'
        },
        'about': {
            'title': f"À Propos - A LAIZ PROD | L'Histoire des Nanfang",
            'description': "Découvrez Flavie et Hervé Nanfang, duo artistique d'exception. Piano, chant, projet Tswefap et excellence musicale camerounaise.",
            'keywords': f"{get_translation('seo_keywords', lang)}, Flavie Nanfang, Hervé Nanfang, histoire, biographie",
            'og_type': 'website'
        },
        'services': {
            'title': f"{get_translation('Services', lang)} - A LAIZ PROD | Prestations Premium",
            'description': f"Découvrez nos {get_translation('Services', lang).lower()} : prestations artistiques, formations IA, sonorisation 3D et événements immersifs.",
            'keywords': f"{get_translation('seo_keywords', lang)}, prestations, sonorisation, événements",
            'og_type': 'website'
        },
        'formations': {
            'title': f"Formations - A LAIZ PROD | Cours Piano et Chant",
            'description': "Formations musicales d'exception par Hervé et Flavie Nanfang. Cours piano, chant, stages intensifs à Yaoundé.",
            'keywords': f"{get_translation('seo_keywords', lang)}, formations, cours piano, cours chant, stages",
            'og_type': 'website'
        },
        'contact': {
            'title': f"{get_translation('Contact', lang)} - A LAIZ PROD | Devis Gratuit",
            'description': f"Contactez A LAIZ PROD pour votre projet musical. Devis gratuit et personnalisé. {get_translation('Contact', lang)} par email, téléphone ou WhatsApp.",
            'keywords': f"{get_translation('seo_keywords', lang)}, devis, contact, projet musical",
            'og_type': 'website'
        },
        'boutique': {
            'title': f"{get_translation('Boutique', lang)} - A LAIZ PROD | Produits Technologiques",
            'description': f"{get_translation('Boutique', lang)} en ligne A LAIZ PROD : applications AR, formations premium, équipements audio innovants.",
            'keywords': f"{get_translation('seo_keywords', lang)}, boutique, applications, formations, AR",
            'og_type': 'product'
        }
    }
    
    return seo_data.get(page, seo_data['accueil'])

# Initialisation de la base de données
def init_db():
    """Initialise la base de données SQLite"""
    conn = sqlite3.connect('alaiz_prod.db')
    cursor = conn.cursor()
    
    # Table des contacts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            project TEXT NOT NULL,
            status TEXT DEFAULT 'nouveau',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            responded_at TIMESTAMP NULL
        )
    ''')
    
    # Table des utilisateurs admin
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table des produits boutique
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            category TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table des commandes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            product_id INTEGER,
            amount DECIMAL(10,2) NOT NULL,
            stripe_payment_id TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Créer un admin par défaut
    admin_exists = cursor.execute('SELECT COUNT(*) FROM admins').fetchone()[0]
    if admin_exists == 0:
        default_password = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO admins (username, email, password_hash) 
            VALUES (?, ?, ?)
        ''', ('admin', 'admin@alaizprod.com', default_password))
        
    # Insérer des produits d'exemple
    product_exists = cursor.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    if product_exists == 0:
        sample_products = [
            ('App Mobile AR', 'Application de réalité augmentée pour l\'apprentissage musical', 29.99, 'digital'),
            ('Casque Audio 3D', 'Casque spatial avec IA pour immersion musicale totale', 299.99, 'hardware'),
            ('Formation Piano IA', 'Cours de piano avec intelligence artificielle', 199.99, 'formation'),
            ('Manuel Interactif', 'Livre augmenté avec exercices IA et simulations 3D', 49.99, 'education')
        ]
        cursor.executemany('''
            INSERT INTO products (name, description, price, category) 
            VALUES (?, ?, ?, ?)
        ''', sample_products)
    
    conn.commit()
    conn.close()

def send_email(to_email, subject, body, is_html=False):
    """Envoie un email via SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['email']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html' if is_html else 'plain', 'utf-8'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['email'], to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False

def save_contact_to_db(name, email, project):
    """Sauvegarde un contact en base de données"""
    try:
        conn = sqlite3.connect('alaiz_prod.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contacts (name, email, project) 
            VALUES (?, ?, ?)
        ''', (name, email, project))
        
        contact_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return contact_id
    except Exception as e:
        print(f"Erreur sauvegarde contact: {e}")
        return None

# Classe Assistant IA
class AIAssistant:
    def __init__(self):
        self.openai_client = None
        self.claude_headers = {
            'Content-Type': 'application/json',
            'x-api-key': AI_CONFIG['claude_api_key'],
            'anthropic-version': '2023-06-01'
        }
        
        if AI_CONFIG['openai_api_key']:
            openai.api_key = AI_CONFIG['openai_api_key']
            self.openai_client = openai
    
    async def get_ai_response(self, message: str, context: str = "customer_service") -> dict:
        """Obtient une réponse IA contextuelle"""
        
        system_prompts = {
            "customer_service": """Tu es l'assistant IA d'A LAIZ PROD, une entreprise innovante spécialisée dans :
            - Prestations artistiques avec technologies immersives (VR/AR)
            - Formations musicales assistées par IA
            - Productions audio avec intelligence artificielle
            - Événements premium (mariages, concerts, corporate)
            
            Réponds de manière professionnelle, chaleureuse et informative. 
            Propose toujours des solutions concrètes et des prochaines étapes.
            Limite tes réponses à 100 mots maximum.""",
            
            "project_analysis": """Tu es un expert en analyse de projets artistiques et technologiques.
            Analyse la demande du client et propose des suggestions pertinentes avec des estimations de prix.
            Focus sur les solutions A LAIZ PROD : IA, VR/AR, audio spatial, formations digitales.""",
            
            "price_estimation": """Tu es un consultant spécialisé dans l'estimation de projets créatifs.
            Fournis des fourchettes de prix réalistes basées sur :
            - Complexité technologique (IA, VR/AR)
            - Durée et ampleur de l'événement
            - Équipements requis
            - Personnalisation demandée"""
        }
        
        try:
            # Fallback sur réponses pré-définies pour commencer
            return self._get_fallback_response(message)
                
        except Exception as e:
            print(f"Erreur IA: {e}")
            return self._get_fallback_response(message)
    
    def _get_fallback_response(self, message: str) -> dict:
        """Réponses de secours intelligentes"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['prix', 'tarif', 'coût', 'budget']):
            response = """Nos tarifs varient selon vos besoins spécifiques. Voici nos gammes :
            
            🎵 **Prestations Live** : 100K - 500K FCFA
            🎓 **Formations** : 12K - 15K FCFA/cours
            🎪 **Mariages** : 250K FCFA (pack complet)
            
            Décrivez votre projet pour un devis personnalisé !"""
            
        elif any(word in message_lower for word in ['mariage', 'wedding']):
            response = """🌟 **Pack Mariage A LAIZ PROD** :
            
            ✨ **Mini** (100K FCFA) : Piano + chant
            💎 **Standard** (150-200K FCFA) : Duo + sono
            🚀 **Complet** (250K FCFA) : Cérémonie + réception
            
            Chaque prestation est personnalisée selon vos rêves !"""
            
        elif any(word in message_lower for word in ['formation', 'cours', 'apprendre']):
            response = """🎓 **Formations A LAIZ PROD** :
            
            🎹 **Piano** (15K FCFA/cours) : Méthode Hervé Nanfang
            🎤 **Chant** (12K FCFA/cours) : Technique Flavie Nanfang
            🎧 **Stages intensifs** (45K FCFA/week-end)
            
            Première consultation gratuite !"""
            
        elif any(word in message_lower for word in ['contact', 'téléphone', 'whatsapp']):
            response = """📞 **Nous Contacter** :
            
            📱 **Téléphone** : +237 682180266
            💬 **WhatsApp** : +237 694723492 (Devis express)
            📧 **Email** : contact@alaizopays.art
            
            Réponse garantie sous 24h !"""
            
        else:
            response = """Bonjour ! Je suis l'assistant IA d'A LAIZ PROD 🎵
            
            Nous sommes spécialisés dans :
            • Prestations musicales (mariages, concerts)
            • Formations piano/chant
            • Sonorisation A Laiz Sono
            
            Comment puis-je vous aider aujourd'hui ?"""
        
        return {
            'response': response,
            'source': 'fallback',
            'confidence': 0.8,
            'timestamp': datetime.now().isoformat()
        }

# Instance globale de l'assistant IA
ai_assistant = AIAssistant()

# ============================================================================
# ROUTES PRINCIPALES - CORRIGÉES POUR UTILISER DES TEMPLATES SÉPARÉS
# ============================================================================

@app.route("/")
def home():
    """Page d'accueil - Utilise index.html"""
    lang = get_locale()
    seo = get_seo_data('accueil')
    return render_template("index.html", page="accueil", lang=lang, seo=seo)

@app.route("/about")
def about():
    """Page À propos - Utilise about.html"""
    lang = get_locale()
    seo = get_seo_data('about')
    return render_template("about.html", page="about", lang=lang, seo=seo)

@app.route("/services")
def services():
    """Page Services - Utilise services.html"""
    lang = get_locale()
    seo = get_seo_data('services')
    return render_template("services.html", page="services", lang=lang, seo=seo)

@app.route("/formations")
def formations():
    """Page Formations - Utilise formations.html"""
    lang = get_locale()
    seo = get_seo_data('formations')
    return render_template("formations.html", page="formations", lang=lang, seo=seo)

@app.route("/contact")
def contact():
    """Page Contact - Utilise contact.html"""
    lang = get_locale()
    seo = get_seo_data('contact')
    return render_template("contact.html", page="contact", lang=lang, seo=seo)

@app.route("/boutique")
def boutique():
    """Page Boutique - Utilise boutique.html ou fallback vers index.html"""
    lang = get_locale()
    seo = get_seo_data('boutique')
    try:
        return render_template("boutique.html", page="boutique", lang=lang, seo=seo)
    except:
        # Fallback si boutique.html n'existe pas encore
        return render_template("index.html", page="boutique", lang=lang, seo=seo)

@app.route("/label")
def label():
    """Page Label - Fallback vers index.html pour l'instant"""
    lang = get_locale()
    seo = get_seo_data('label')
    return render_template("index.html", page="label", lang=lang, seo=seo)

@app.route("/artiste")
def artiste():
    """Page Artiste - Fallback vers index.html pour l'instant"""
    lang = get_locale()
    seo = get_seo_data('artiste')
    return render_template("index.html", page="artiste", lang=lang, seo=seo)

@app.route("/admin")
def admin_dashboard():
    """Dashboard admin - Utilise admin.html"""
    return render_template("admin.html")

# Route de test pour vérifier le routage
@app.route("/test")
def test_route():
    """Route de test pour vérifier que le routage fonctionne"""
    return """
    <h1 style="color: green;">✅ ROUTAGE CORRIGÉ !</h1>
    <p>Si vous voyez cette page, le problème est résolu.</p>
    <ul>
        <li><a href="/">Accueil</a></li>
        <li><a href="/about">À Propos</a></li>
        <li><a href="/services">Services</a></li>
        <li><a href="/formations">Formations</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
    """

# ============================================================================
# API ROUTES
# ============================================================================

@app.route("/api/weather")
def api_weather():
    """API pour les données météo simulées"""
    weather_data = {
        "temperature": 24,
        "condition": "Partiellement nuageux",
        "icon": "🌤️",
        "city": "Yaoundé",
        "humidity": 72,
        "wind": "8 km/h"
    }
    return jsonify(weather_data)

@app.route("/api/ai-chat", methods=["POST"])
async def ai_chat():
    """API pour le chat IA"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', 'customer_service')
        
        ai_response = await ai_assistant.get_ai_response(message, context)
        return jsonify(ai_response)
        
    except Exception as e:
        return jsonify({
            'response': 'Désolé, je rencontre un problème technique. Pouvez-vous reformuler votre question ?',
            'source': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route("/api/smart-form", methods=["POST"])
async def smart_form():
    """API pour l'analyse IA du formulaire"""
    try:
        data = request.get_json()
        description = data.get('description', '').lower()
        
        suggestions = []
        
        if 'mariage' in description:
            suggestions.extend([
                '💍 Pack Mariage Complet - 250 000 FCFA',
                '🎵 Piano-bar Standard - 150 000 FCFA',
                '💒 Cérémonie musicale - 100 000 FCFA'
            ])
        
        if 'formation' in description:
            suggestions.extend([
                '🎓 Cours Piano Hervé Nanfang - 15 000 FCFA',
                '🎤 Cours Chant Flavie Nanfang - 12 000 FCFA',
                '🎹 Stage intensif week-end - 45 000 FCFA'
            ])
        
        if 'concert' in description:
            suggestions.extend([
                '🎤 Orchestre Prestige - 500 000 FCFA',
                '🔊 Sonorisation premium - 160 000 FCFA',
                '🎥 Prestation complète - Devis sur mesure'
            ])
        
        if not suggestions:
            suggestions = [
                '🎯 Consultation personnalisée gratuite',
                '📞 Entretien avec nos experts',
                '💡 Analyse de vos besoins spécifiques'
            ]
        
        return jsonify({
            'suggestions': suggestions,
            'analysis': 'Analyse IA terminée',
            'confidence': 95
        })
        
    except Exception as e:
        return jsonify({
            'suggestions': ['🎯 Consultation personnalisée recommandée'],
            'error': str(e)
        }), 500

@app.route("/api/contact", methods=["POST"])
def submit_contact():
    """API pour soumission du formulaire de contact avec email réel"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        project = data.get('project')
        
        # Sauvegarder en base de données
        contact_id = save_contact_to_db(name, email, project)
        
        if contact_id:
            # Email à l'admin
            admin_subject = f"Nouveau contact A LAIZ PROD - {name}"
            admin_body = f"""
            <h2>Nouveau message de contact</h2>
            <p><strong>Nom:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Projet:</strong></p>
            <p>{project}</p>
            <p><strong>ID Contact:</strong> {contact_id}</p>
            <p><strong>Date:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            """
            
            # Email de confirmation au client
            client_subject = "Confirmation de réception - A LAIZ PROD"
            client_body = f"""
            <h2>Bonjour {name},</h2>
            <p>Nous avons bien reçu votre demande concernant :</p>
            <blockquote>{project}</blockquote>
            <p>Notre équipe va analyser votre projet et vous recontacter sous 24h.</p>
            <p>En cas d'urgence, contactez-nous directement :</p>
            <p>📞 Téléphone : +237 682180266</p>
            <p>💬 WhatsApp : +237 694723492</p>
            <br>
            <p>Cordialement,<br>L'équipe A LAIZ PROD</p>
            """
            
            # Envoyer les emails
            send_email(EMAIL_CONFIG['admin_email'], admin_subject, admin_body, True)
            send_email(email, client_subject, client_body, True)
            
            return jsonify({
                'success': True,
                'message': 'Message envoyé avec succès !',
                'contact_id': contact_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la sauvegarde'
            }), 500
            
    except Exception as e:
        print(f"Erreur API contact: {e}")
        return jsonify({
            'success': False,
            'message': 'Erreur serveur'
        }), 500

# ============================================================================
# GESTION DES ERREURS
# ============================================================================

@app.errorhandler(404)
def page_not_found(e):
    """Page 404 personnalisée"""
    return render_template('index.html', page='404'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Page 500 personnalisée"""
    return render_template('index.html', page='500'), 500

# ============================================================================
# INITIALISATION ET LANCEMENT
# ============================================================================

# Initialiser la base de données au démarrage
with app.app_context():
    init_db()

if __name__ == '__main__':
    # Configuration selon l'environnement
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 A LAIZ PROD - Démarrage de l'application")
    print(f"🌐 URL: {app.config['SITE_URL']}")
    print(f"🔧 Mode debug: {debug_mode}")
    print(f"📧 Email configuré: {EMAIL_CONFIG['email']}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
