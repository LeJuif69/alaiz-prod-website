from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_mail import Mail, Message
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'alaiz-prod-secret-key-2024'

# Configuration email pour formulaire de contact
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT') or 587)
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') or 'votre_email@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS') or 'votre_mot_de_passe'

mail = Mail(app)

# ==============================================
# DONNÉES DU LABEL MUSICAL A LAIZ PROD
# ==============================================

# Informations principales du label
LABEL_INFO = {
    'name': 'A Laiz Prod',
    'tagline': 'Label Musical Camerounais',
    'description': 'Plateforme de créations artistiques et collaborations musicales d\'excellence',
    'founded': 2009,
    'location': 'Yaoundé, Cameroun',
    'vision': 'Révéler et fédérer les talents camerounais et internationaux autour de créations musicales d\'exception',
    'director': {
        'name': 'Hervé Nanfang',
        'title': 'Fondateur & Directeur Artistique',
        'bio': 'Pianiste de formation classique et jazz, pédagogue reconnu et visionnaire culturel. Hervé dirige A Laiz Prod avec une approche unique qui unit tradition camerounaise et innovation musicale contemporaine.',
        'specialties': [
            'Direction Artistique',
            'Piano Classique & Jazz', 
            'Pédagogie Musicale',
            'Arrangements & Compositions',
            'Projet Culturel Tswefap',
            'Collaborations Internationales'
        ],
        'phone': os.environ.get('DIRECTOR_PHONE') or '+237 XXX XXX XXX',
        'email': os.environ.get('DIRECTOR_EMAIL') or 'herve@alaizprod.com'
    },
    'contact': {
        'main_phone': os.environ.get('DIRECTOR_PHONE') or '+237 XXX XXX XXX',
        'email': os.environ.get('CONTACT_EMAIL') or 'contact@alaizprod.com',
        'booking_email': os.environ.get('BOOKING_EMAIL') or 'booking@alaizprod.com',
        'address': 'Yaoundé, Cameroun',
        'social': {
            'facebook': os.environ.get('FACEBOOK_URL') or 'https://facebook.com/alaizprod',
            'instagram': os.environ.get('INSTAGRAM_URL') or 'https://instagram.com/alaizprod',
            'youtube': os.environ.get('YOUTUBE_URL') or 'https://youtube.com/alaizprod',
            'linkedin': os.environ.get('LINKEDIN_URL') or 'https://linkedin.com/in/hervenanfang',
            'whatsapp': os.environ.get('WHATSAPP_URL') or 'https://wa.me/237XXXXXXXXX'
        }
    }
}

# Types de collaborations artistiques
COLLABORATIONS = {
    'vocal_artists': {
        'title': 'Artistes Vocaux',
        'description': 'Chanteuses et chanteurs d\'exception pour projets variés',
        'genres': ['Gospel', 'Jazz Vocal', 'Afro-contemporain', 'Variété Française', 'World Music'],
        'icon': 'fas fa-microphone'
    },
    'instrumentalists': {
        'title': 'Musiciens Instrumentistes',
        'description': 'Violonistes, guitaristes, percussionnistes... Une famille d\'instrumentistes',
        'genres': ['Cordes', 'Percussions', 'Vents', 'Piano', 'Guitares'],
        'icon': 'fas fa-guitar'
    },
    'creators': {
        'title': 'Créateurs & Arrangeurs',
        'description': 'Compositeurs, arrangeurs, producteurs pour visions artistiques',
        'genres': ['Composition', 'Arrangement', 'Production', 'Direction Musicale'],
        'icon': 'fas fa-palette'
    },
    'international': {
        'title': 'Partenaires Internationaux',
        'description': 'Collaborations avec artistes et institutions culturelles internationales',
        'genres': ['Europe', 'Afrique', 'Amérique', 'Asie'],
        'icon': 'fas fa-globe'
    }
}

# Services du label
SERVICES_DATA = {
    'productions': {
        'id': 'productions',
        'title': 'Productions Musicales',
        'icon': 'fas fa-music',
        'description': 'Créations artistiques collaboratives pour tous vos événements.',
        'full_description': 'Nos productions mobilisent un réseau d\'artistes sélectionnés selon l\'ambiance souhaitée. Piano, voix, instruments d\'accompagnement... chaque prestation est une création unique.',
        'types': ['Piano-Bar Collaboratif', 'Formations Musicales Variables', 'Arrangements Sur Mesure']
    },
    'mariages': {
        'id': 'mariages',
        'title': 'Créations Matrimoniales',
        'icon': 'fas fa-heart',
        'description': 'Compositions musicales sur mesure pour votre union.',
        'full_description': 'Votre mariage mérite une bande sonore exceptionnelle. A Laiz Prod compose une équipe artistique personnalisée selon vos goûts et traditions.',
        'types': ['Cérémonie Personnalisée', 'Cocktail Collaboratif', 'Soirée Signature']
    },
    'concerts': {
        'id': 'concerts',
        'title': 'Productions Scéniques',
        'icon': 'fas fa-microphone',
        'description': 'Spectacles live mémorables avec collaborations artistiques.',
        'full_description': 'De l\'intimité du récital aux grandes productions, A Laiz Prod coordonne des spectacles live avec collaborations artistiques et créations originales.',
        'types': ['Récitals Intimistes', 'Concerts Fusion', 'Grandes Productions']
    },
    'formations': {
        'id': 'formations',
        'title': 'Formations Musicales',
        'icon': 'fas fa-graduation-cap',
        'description': 'Excellence pédagogique par Hervé Nanfang.',
        'full_description': 'Méthodes pédagogiques innovantes adaptées à tous niveaux. Formation technique et développement artistique par le directeur du label.',
        'types': ['Cours Particuliers', 'Masterclass', 'Stages Intensifs']
    },
    'sonorisation': {
        'id': 'sonorisation',
        'title': 'A Laiz Sono',
        'icon': 'fas fa-volume-up',
        'description': 'Solutions techniques professionnelles.',
        'full_description': 'Équipements de qualité professionnelle et service technique expert pour accompagner nos productions et événements externes.',
        'types': ['Sonorisation Standard', 'Solutions Premium', 'Régie Complète']
    },
    'tswefap': {
        'id': 'tswefap',
        'title': 'Projet Culturel Tswefap',
        'icon': 'fas fa-globe-africa',
        'description': 'Préservation du patrimoine linguistique Batoufam.',
        'full_description': 'Initiative culturelle unique alliant tradition et innovation technologique pour valoriser et préserver la richesse linguistique camerounaise.',
        'types': ['Documentation Culturelle', 'Applications Numériques', 'Transmission Éducative']
    }
}

# Statistiques du label
LABEL_STATS = {
    'experience': 15,      # Années d'existence
    'projects': 500,       # Projets réalisés
    'collaborators': 50,   # Artistes collaborateurs
    'students': 1000,      # Élèves formés
    'publications': 12     # Publications pédagogiques
}

# ==============================================
# ROUTES DE L'APPLICATION
# ==============================================

@app.route('/')
def index():
    """Page d'accueil - Label Musical"""
    return render_template('index.html', 
                         label=LABEL_INFO,
                         services=SERVICES_DATA,
                         collaborations=COLLABORATIONS,
                         stats=LABEL_STATS)

@app.route('/services')
def services():
    """Page services - Productions du Label"""
    return render_template('services.html', 
                         label=LABEL_INFO,
                         services=SERVICES_DATA,
                         collaborations=COLLABORATIONS)

@app.route('/about')
def about():
    """Page à propos - Vision du Label"""
    return render_template('about.html', 
                         label=LABEL_INFO,
                         collaborations=COLLABORATIONS)

@app.route('/formations')
def formations():
    """Page formations - Pédagogie du Directeur"""
    # Cours disponibles avec Hervé Nanfang
    formation_courses = [
        {
            'name': 'Piano Débutant',
            'level': 'Débutant',
            'duration': '3 mois minimum',
            'price': '25.000 FCFA/mois',
            'schedule': 'Mercredi et Samedi 14h-16h',
            'description': 'Apprentissage des bases du piano : posture, gammes, accords simples et premiers morceaux.'
        },
        {
            'name': 'Piano Intermédiaire', 
            'level': 'Intermédiaire',
            'duration': '6 mois',
            'price': '30.000 FCFA/mois',
            'schedule': 'Mardi et Jeudi 16h-18h',
            'description': 'Perfectionnement technique, harmonie avancée, répertoire classique et jazz.'
        },
        {
            'name': 'Chant & Interprétation',
            'level': 'Tous niveaux',
            'duration': '6 mois',
            'price': '30.000 FCFA/mois', 
            'schedule': 'Lundi et Mercredi 18h-20h',
            'description': 'Technique vocale, respiration, interprétation, préparation scénique.'
        },
        {
            'name': 'Théorie Musicale',
            'level': 'Tous niveaux',
            'duration': '4 mois',
            'price': '20.000 FCFA/mois',
            'schedule': 'Vendredi 16h-18h',
            'description': 'Solfège, harmonie, analyse musicale, composition de base.'
        },
        {
            'name': 'Direction Artistique',
            'level': 'Avancé',
            'duration': 'Sur projet',
            'price': 'Sur devis',
            'schedule': 'Planning personnalisé',
            'description': 'Formation à la direction musicale, arrangement, production artistique.'
        }
    ]
    
    return render_template('formations.html', 
                         label=LABEL_INFO,
                         courses=formation_courses,
                         director=LABEL_INFO['director'])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Page contact - Formulaire de contact du label"""
    if request.method == 'POST':
        # Récupération des données
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip() 
        phone = request.form.get('phone', '').strip()
        project_type = request.form.get('project_type', '').strip()
        event_date = request.form.get('event_date', '').strip()
        location = request.form.get('location', '').strip()
        budget = request.form.get('budget', '').strip()
        message = request.form.get('message', '').strip()
        newsletter = request.form.get('newsletter')
        
        # Validation
        if not all([name, email, phone]):
            flash('Veuillez remplir tous les champs obligatoires (nom, email, téléphone)', 'error')
            return render_template('contact.html', label=LABEL_INFO)
        
        # Tentative d'envoi d'email
        try:
            subject = f'Nouvelle demande - A Laiz Prod : {project_type or "Non spécifié"}'
            
            email_body = f"""
Nouvelle demande reçue via le site A Laiz Prod :

INFORMATIONS CLIENT :
- Nom : {name}
- Email : {email}
- Téléphone : {phone}

DÉTAILS PROJET :
- Type : {project_type or 'Non spécifié'}
- Date souhaitée : {event_date or 'Non spécifiée'}
- Lieu : {location or 'Non spécifié'}
- Budget approximatif : {budget or 'Non spécifié'}

MESSAGE :
{message or 'Aucun message spécifique'}

NEWSLETTER : {'Oui' if newsletter else 'Non'}

---
Email automatique depuis alaizopays.art
Date : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
            """
            
            # Email à A Laiz Prod
            msg = Message(
                subject=subject,
                sender=app.config['MAIL_USERNAME'],
                recipients=[LABEL_INFO['contact']['email']],
                body=email_body
            )
            
            # Email de confirmation au client
            confirmation_msg = Message(
                subject='Votre demande - A Laiz Prod',
                sender=app.config['MAIL_USERNAME'],
                recipients=[email],
                body=f"""
Bonjour {name},

Merci pour votre intérêt pour A Laiz Prod, label musical camerounais.

Nous avons bien reçu votre demande concernant : "{project_type or 'votre projet musical'}"

Notre équipe vous recontactera dans les plus brefs délais (sous 24h maximum) pour discuter de votre projet et vous proposer une collaboration sur mesure.

En attendant, n'hésitez pas à nous appeler directement :
- Hervé Nanfang (Directeur Artistique) : {LABEL_INFO['director']['phone']}

Cordialement,
L'équipe A Laiz Prod
Excellence musicale camerounaise depuis 2009
                """
            )
            
            mail.send(msg)
            mail.send(confirmation_msg)
            
            flash('Votre demande a été envoyée avec succès ! Nous vous recontacterons sous 24h.', 'success')
            
        except Exception as e:
            flash('Erreur lors de l\'envoi de l\'email. Veuillez nous contacter directement.', 'error')
            print(f"Erreur envoi email: {e}")
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html', label=LABEL_INFO)

@app.route('/api/stats')
def api_stats():
    """API pour les statistiques du label"""
    return jsonify(LABEL_STATS)

@app.route('/api/collaborations')
def api_collaborations():
    """API pour les informations de collaborations"""
    return jsonify(COLLABORATIONS)

@app.errorhandler(404)
def page_not_found(e):
    """Page d'erreur 404 personnalisée"""
    return "Page not found", 404

@app.errorhandler(500)
def internal_server_error(e):
    """Page d'erreur 500 personnalisée"""
    return "Internal server error", 500

# ==============================================
# LANCEMENT DE L'APPLICATION
# ==============================================

if __name__ == '__main__':
    # Configuration pour développement local
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(
        debug=debug_mode,
        host='0.0.0.0', 
        port=port
    )
