from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_mail import Mail, Message
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'alaiz-prod-secret-key-2024'

# Configuration email pour formulaire de contact
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') or 'votre_email@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS') or 'votre_mot_de_passe'

mail = Mail(app)

# Données des services
SERVICES_DATA = {
    'piano_bar': {
        'id': 'piano-bar',
        'title': 'Piano-Bar',
        'icon': 'fas fa-music',
        'description': 'Ambiances musicales raffinées pour vos soirées privées, restaurants et hôtels.',
        'full_description': 'Créez une atmosphère unique avec nos prestations piano-bar. Du jazz aux standards internationaux, nos performances s\'adaptent à l\'ambiance souhaitée.',
        'packages': [
            {
                'name': 'Formule Mini',
                'duration': '2 heures',
                'price': '75.000 FCFA',
                'includes': ['Piano et chant', 'Répertoire varié', 'Matériel sonore']
            },
            {
                'name': 'Formule Standard', 
                'duration': '3 heures',
                'price': '100.000 FCFA',
                'includes': ['Piano et chant', 'Répertoire étendu', 'Matériel sonore', 'Pause incluse']
            },
            {
                'name': 'Formule Premium',
                'duration': '4 heures',
                'price': '130.000 FCFA', 
                'includes': ['Piano et chant', 'Répertoire personnalisé', 'Matériel sonore pro', 'Animation entre sets']
            }
        ]
    },
    'mariages': {
        'id': 'mariages',
        'title': 'Mariages',
        'icon': 'fas fa-heart',
        'description': 'Célébrez votre union avec une musique sur mesure pour un jour inoubliable.',
        'full_description': 'Votre mariage mérite une bande sonore parfaite. Nous personnalisons chaque moment musical selon vos goûts et traditions.',
        'packages': [
            {
                'name': 'Cérémonie Simple',
                'duration': 'Cérémonie uniquement',
                'price': 'Sur devis',
                'includes': ['Musique d\'entrée', 'Accompagnement cérémonie', 'Musique de sortie']
            },
            {
                'name': 'Cérémonie + Cocktail',
                'duration': 'Cérémonie + 2h cocktail',
                'price': 'Sur devis',
                'includes': ['Cérémonie complète', 'Animation cocktail', 'Matériel sonore', 'Répertoire adapté']
            },
            {
                'name': 'Mariage Complet',
                'duration': 'Toute la journée',
                'price': 'Sur devis',
                'includes': ['Cérémonie', 'Cocktail', 'Dîner', 'Soirée dansante', 'Sonorisation complète']
            }
        ]
    },
    'concerts': {
        'id': 'concerts',
        'title': 'Concerts',
        'icon': 'fas fa-microphone',
        'description': 'Spectacles live mémorables pour festivals et événements culturels.',
        'full_description': 'Des performances scéniques authentiques qui marquent les esprits. Jazz, world music, créations originales.',
        'packages': [
            {
                'name': 'Concert Intimiste',
                'duration': '1h30',
                'price': 'Sur devis',
                'includes': ['Performance scénique', 'Répertoire concert', 'Sound check']
            },
            {
                'name': 'Concert Festival',
                'duration': '2h',
                'price': 'Sur devis', 
                'includes': ['Performance complète', 'Matériel scénique', 'Technique son/éclairage']
            }
        ]
    },
    'formations': {
        'id': 'formations',
        'title': 'Formations Musicales',
        'icon': 'fas fa-graduation-cap',
        'description': 'Cours de piano, chant et théorie musicale par Hervé Nanfang.',
        'full_description': 'Méthodes pédagogiques éprouvées adaptées à tous niveaux. De l\'initiation au perfectionnement professionnel.',
        'packages': [
            {
                'name': 'Cours Individuels',
                'duration': '1h/semaine',
                'price': '25.000 FCFA/mois',
                'includes': ['8 séances mensuelles', 'Matériel pédagogique', 'Suivi personnalisé']
            },
            {
                'name': 'Stages Intensifs',
                'duration': 'Week-end',
                'price': '40.000 FCFA',
                'includes': ['2 jours formation', 'Matériel inclus', 'Certificat']
            }
        ]
    },
    'sono': {
        'id': 'sono',
        'title': 'A Laiz Sono',
        'icon': 'fas fa-volume-up',
        'description': 'Solutions complètes de sonorisation professionnelle.',
        'full_description': 'Équipements de qualité professionnelle et service technique expert pour tous vos événements.',
        'packages': [
            {
                'name': 'Sonorisation Standard',
                'duration': 'Selon événement',
                'price': 'Sur devis',
                'includes': ['Matériel son', 'Installation', 'Technicien sur site']
            },
            {
                'name': 'Sonorisation Premium',
                'duration': 'Selon événement', 
                'price': 'Sur devis',
                'includes': ['Matériel professionnel', 'Éclairage', 'Technicien dédié', 'Assistance complète']
            }
        ]
    }
}

# Données équipe
TEAM_DATA = {
    'flavie': {
        'name': 'Flavie Nanfang',
        'role': 'Chanteuse Professionnelle',
        'bio': 'Chanteuse polyvalente aux registres étendus, Flavie maîtrise aussi bien les standards jazz que les rythmes afro-contemporains. Sa présence scénique magnétique et sa capacité à créer une connexion émotionnelle instantanée avec le public font d\'elle l\'une des voix les plus appréciées du paysage musical camerounais.',
        'specialties': ['Jazz & Standards', 'Musique Afro-contemporaine', 'Gospel & Spiritual', 'Variété Française'],
        'phone': '+237 XXX XXX XXX'  # À remplacer par le vrai numéro
    },
    'herve': {
        'name': 'Hervé Nanfang',
        'role': 'Pianiste & Pédagogue',
        'bio': 'Pianiste de formation classique et jazz, Hervé est également un enseignant reconnu et auteur de plusieurs ouvrages pédagogiques. Sa maîtrise technique exceptionnelle se double d\'une approche pédagogique innovante qui a formé des centaines d\'élèves. Passionné par la préservation culturelle, il développe le projet Tswefap.',
        'specialties': ['Piano Classique & Jazz', 'Pédagogie Musicale', 'Arrangement Musical', 'Projet Culturel Tswefap'],
        'phone': '+237 XXX XXX XXX'  # À remplacer par le vrai numéro
    }
}

# ROUTES
@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html', services=SERVICES_DATA, team=TEAM_DATA)

@app.route('/services')
def services():
    """Page services détaillée"""
    return render_template('services.html', services=SERVICES_DATA)

@app.route('/about')
def about():
    """Page à propos détaillée"""
    return render_template('about.html', team=TEAM_DATA)

@app.route('/formations')
def formations():
    """Page formations détaillée"""
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
            'name': 'Chant Professionnel',
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
        }
    ]
    return render_template('formations.html', courses=formation_courses, team=TEAM_DATA)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Page contact avec formulaire"""
    if request.method == 'POST':
        # Récupération des données du formulaire
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip() 
        phone = request.form.get('phone', '').strip()
        event_type = request.form.get('event_type', '').strip()
        event_date = request.form.get('event_date', '').strip()
        location = request.form.get('location', '').strip()
        guests = request.form.get('guests', '').strip()
        message = request.form.get('message', '').strip()
        newsletter = request.form.get('newsletter')
        
        # Validation
        if not all([name, email, phone]):
            flash('Veuillez remplir tous les champs obligatoires (nom, email, téléphone)', 'error')
            return render_template('contact.html')
        
        # Tentative d'envoi d'email
        try:
            subject = f'Nouvelle demande de devis - {event_type or "Non spécifié"}'
            
            email_body = f"""
Nouvelle demande de devis reçue via le site A Laiz Prod :

INFORMATIONS CLIENT :
- Nom : {name}
- Email : {email}
- Téléphone : {phone}

DÉTAILS ÉVÉNEMENT :
- Type : {event_type or 'Non spécifié'}
- Date souhaitée : {event_date or 'Non spécifiée'}
- Lieu : {location or 'Non spécifié'}
- Nombre d'invités : {guests or 'Non spécifié'}

MESSAGE :
{message or 'Aucun message spécifique'}

NEWSLETTER : {'Oui' if newsletter else 'Non'}

---
Email envoyé automatiquement depuis alaizopays.art
Date : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
            """
            
            msg = Message(
                subject=subject,
                sender=app.config['MAIL_USERNAME'],
                recipients=['contact@alaizprod.com'],  # Votre email de réception
                body=email_body
            )
            
            # Email de confirmation au client
            confirmation_msg = Message(
                subject='Confirmation de votre demande - A Laiz Prod',
                sender=app.config['MAIL_USERNAME'],
                recipients=[email],
                body=f"""
Bonjour {name},

Merci pour votre demande de devis pour un événement de type "{event_type or 'non spécifié'}".

Nous avons bien reçu votre message et nous vous recontacterons dans les plus brefs délais (sous 24h maximum).

En attendant, n'hésitez pas à nous appeler directement :
- Flavie : +237 XXX XXX XXX
- Hervé : +237 XXX XXX XXX

À bientôt pour votre projet musical !

L'équipe A Laiz Prod
Excellence musicale camerounaise
                """
            )
            
            mail.send(msg)
            mail.send(confirmation_msg)
            
            flash('Votre demande a été envoyée avec succès ! Nous vous recontacterons sous 24h.', 'success')
            
        except Exception as e:
            # En cas d'échec d'envoi d'email, on confirme quand même la réception
            flash('Votre demande a été reçue ! Nous vous recontacterons très bientôt.', 'success')
            # Log de l'erreur pour debug (optionnel)
            print(f"Erreur envoi email: {e}")
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/api/stats')
def api_stats():
    """API pour les statistiques animées"""
    stats = {
        'experience': 15,
        'events': 500,
        'mariages': 200,
        'students': 1000,
        'publications': 12
    }
    return jsonify(stats)

@app.errorhandler(404)
def page_not_found(e):
    """Page d'erreur 404 personnalisée"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Page d'erreur 500 personnalisée"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Configuration pour développement local
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Configuration pour production (Render, Heroku, etc.)
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
