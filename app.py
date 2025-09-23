from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Configuration Flask depuis .env
app.secret_key = os.getenv('SECRET_KEY', 'alaiz-prod-2010-herve-nanfang')
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# DONNÉES A LAIZ PROD (avec variables d'environnement en priorité)
ALAIZ_DATA = {
    "nom": "A Laiz Prod",
    "slogan": "Tradition. Innovation. Émotion.",
    "directeur": "Hervé Nanfang",
    
    # Téléphones (variables d'environnement en priorité)
    "telephones": [
        os.getenv('DIRECTOR_PHONE', '+237 682 180 266'),
        '+237 694 723 492'  # Téléphone secondaire fixe
    ],
    
    # Emails (variables d'environnement en priorité)
    "emails": {
        "contact": os.getenv('CONTACT_EMAIL', 'contact@alaizopays.art'),
        "booking": os.getenv('BOOKING_EMAIL', 'booking@alaizopays.art'),
        "formation": os.getenv('DIRECTOR_EMAIL', 'herve@alaizprod.com')
    },
    
    "adresse": "Rue Nachtigall, Melen, Yaoundé – Cameroun",
    "annee_fondation": 2010,
    
    # Réseaux sociaux (variables d'environnement en priorité)
    "reseaux_sociaux": {
        "facebook": os.getenv('FACEBOOK_URL', 'https://facebook.com/alaizprodcameroun'),
        "instagram": os.getenv('INSTAGRAM_URL', 'https://instagram.com/alaizprod_officiel'),
        "youtube": os.getenv('YOUTUBE_URL', 'https://youtube.com/@alaizprod'),
        "linkedin": os.getenv('LINKEDIN_URL', 'https://linkedin.com/in/hervenanfang'),
        "whatsapp": os.getenv('WHATSAPP_URL', 'https://wa.me/237694723492')
    },
    
    # Analytics (optionnel)
    "google_analytics_id": os.getenv('GOOGLE_ANALYTICS_ID', ''),
    "facebook_pixel_id": os.getenv('FACEBOOK_PIXEL_ID', ''),
    
    # Section Label
    "description_label": "Créé en 2010 par Hervé Nanfang, A Laiz Prod est un label musical et artistique qui réunit la passion des musiques d'hier et d'aujourd'hui. Notre mission : faire dialoguer l'héritage culturel africain et l'exigence des standards internationaux.",
    
    "specialites": [
        "Production et direction artistique",
        "Événementiel live (concerts, mariages, piano-bar)",
        "Formation et pédagogie musicale",
        "Location d'instruments professionnels"
    ],
    
    "realisations_phares": [
        "Album Shepo (2013) + nouvel album en préparation",
        "Bafoussam Worship Experience (30 novembre 2025)",
        "Inauguration de MikeLand (Bénin)",
        "Première partie d'Asalfo (Magic System)",
        "Première partie de Diam's (2010)",
        "Yafé (Yaoundé en Fête, 2012)",
        "Africa Star Dakar 2010",
        "Coupe d'Afrique de Musique CAFRIM 2013 - Trophée du Meilleur Compositeur"
    ],
    
    "artistes_collaborations": [
        "Aladji Touré", "Étienne Bappé", "Kares Fotso", "Lady Ponce",
        "Richard Amougou", "Tala André Marie", "Stypak Samo", "Angélique Kidjo",
        "Sagbohan Danialou", "Rikos Campos", "Toofan", "Big Caïd"
    ],
    
    # Section Pédagogie
    "description_pedagogie": "Chez A Laiz Prod, la transmission du savoir fait partie intégrante de notre mission. Sous la direction d'Hervé Nanfang, musicologue et pédagogue, nous proposons des formations alliant tradition africaine et techniques modernes.",
    
    "formations": [
        {
            "nom": "MAO – Musique Assistée par Ordinateur",
            "description": "Initiation et perfectionnement aux logiciels professionnels pour la composition et la production musicale."
        },
        {
            "nom": "Musicologie appliquée aux médias visuels", 
            "description": "Analyse et création de musiques de films, documentaires, publicités et jeux vidéo."
        },
        {
            "nom": "Techniques de composition musicale",
            "description": "Apprendre à écrire, arranger et orchestrer des œuvres originales dans différents styles."
        },
        {
            "nom": "Classes spécialisées",
            "description": "Encadrement d'enfants et d'adultes à besoins spécifiques, avec une approche inclusive."
        }
    ],
    
    "partenaires": [
        "École Supérieure des Arts du Spectacle de Lomé (ESAS)",
        "Institut Supérieur des Métiers des Arts du Bénin (ISMA)", 
        "Collège Excellence et PADIPS (Yaoundé)"
    ],
    
    # Instruments
    "instruments": [
        "Yamaha Genos", "Yamaha Tyros", "Roland Fantom", "Korg PA5X",
        "Yamaha SX900", "Yamaha SX600", "Sonorisation professionnelle", "Éclairage scénique"
    ],
    
    # Section Blog
    "articles_blog": [
        {
            "titre": "Dans les coulisses d'A Laiz Prod : rencontre avec Aladji Touré",
            "categorie": "Portrait d'Artiste",
            "date": "15 mars 2024",
            "resume": "Découverte de la collaboration entre Aladji Touré et Hervé Nanfang, entre tradition et innovation musicale.",
            "image": "aladji-toure.jpg"
        },
        {
            "titre": "Bafoussam Worship Experience 2025 : un événement gospel exceptionnel",
            "categorie": "Événements",
            "date": "10 mars 2024", 
            "resume": "Présentation du concert gospel du 30 novembre 2025 avec Hervé Nanfang et des artistes de la scène camerounaise.",
            "image": "bafoussam-worship.jpg"
        },
        {
            "titre": "Atelier Composition Musicale & MAO - Session 2025",
            "categorie": "Formations",
            "date": "5 mars 2024",
            "resume": "Détails de la nouvelle session de formation en composition et MAO dirigée par Hervé Nanfang.",
            "image": "atelier-mao.jpg"
        }
    ],
    
    "categories_blog": ["Actus du Label", "Portrait d'Artiste", "Formations", "Événements", "Culture & Innovation"]
}

@app.route('/')
def accueil():
    annee_courante = datetime.now().year
    annees_experience = annee_courante - ALAIZ_DATA["annee_fondation"]
    
    context = {
        **ALAIZ_DATA,
        "annees_experience": annees_experience,
        "annee_courante": annee_courante,
        "page_title": f"{ALAIZ_DATA['nom']} - {ALAIZ_DATA['slogan']}",
        "page_description": "Label musical camerounais fondé en 2010 par Hervé Nanfang. Production musicale, événements, formations et location d'instruments."
    }
    return render_template('index.html', **context)

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        try:
            # Récupération des données du formulaire
            nom = request.form.get('nom', '').strip()
            email = request.form.get('email', '').strip()
            telephone = request.form.get('telephone', '').strip()
            service = request.form.get('service', '').strip()
            message = request.form.get('message', '').strip()
            
            # Validation des champs obligatoires
            if not nom or not email or not message:
                return jsonify({
                    'success': False, 
                    'message': 'Le nom, l\'email et le message sont obligatoires.'
                })
            
            # Validation basique de l'email
            if '@' not in email or '.' not in email:
                return jsonify({
                    'success': False,
                    'message': 'Veuillez entrer une adresse email valide.'
                })
            
            # Envoi de l'email
            resultat_envoi = envoyer_email_contact(nom, email, telephone, service, message)
            
            if resultat_envoi:
                # Log de la soumission
                app.logger.info(f'Nouveau contact: {nom} ({email}) - Service: {service}')
                
                return jsonify({
                    'success': True, 
                    'message': 'Merci pour votre message ! Hervé vous contactera rapidement.'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Erreur d\'envoi d\'email. Contactez-nous directement par téléphone.'
                })
            
        except Exception as e:
            app.logger.error(f'Erreur formulaire contact: {str(e)}')
            return jsonify({
                'success': False, 
                'message': 'Une erreur s\'est produite. Veuillez réessayer ou nous contacter directement par téléphone.'
            })

def envoyer_email_contact(nom, email, telephone, service, message):
    """Fonction pour envoyer les emails de contact avec configuration depuis .env"""
    try:
        # Configuration SMTP depuis les variables d'environnement
        smtp_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('MAIL_PORT', 587))
        smtp_username = os.getenv('EMAIL_USER')
        smtp_password = os.getenv('EMAIL_PASS')
        
        # Vérification de la configuration SMTP
        if not all([smtp_server, smtp_username, smtp_password]):
            app.logger.warning('Configuration SMTP incomplète dans .env - email non envoyé')
            return False
        
        # Construction du message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = ALAIZ_DATA["emails"]["contact"]
        msg['Subject'] = f'✨ Nouveau message A Laiz Prod - {service}'
        
        # Corps du message formaté
        corps_message = f"""
        NOUVEAU MESSAGE - SITE A LAIZ PROD
        {'=' * 40}
        
        📋 INFORMATIONS CLIENT :
        • Nom : {nom}
        • Email : {email}
        • Téléphone : {telephone or 'Non renseigné'}
        • Service souhaité : {service or 'Non spécifié'}
        
        💬 MESSAGE :
        {message}
        
        {'-' * 40}
        📧 Envoyé depuis le formulaire de contact
        🌐 Site : https://alaizopays.art
        ⏰ Date : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
        """
        
        msg.attach(MIMEText(corps_message, 'plain', 'utf-8'))
        
        # Envoi via SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        app.logger.info(f'Email de contact envoyé avec succès pour {email}')
        return True
        
    except smtplib.SMTPAuthenticationError:
        app.logger.error('Erreur d\'authentification SMTP - Vérifiez EMAIL_USER et EMAIL_PASS dans .env')
        return False
    except Exception as e:
        app.logger.error(f'Erreur envoi email: {str(e)}')
        return False

@app.route('/health')
def health_check():
    """Endpoint de santé pour le monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'A Laiz Prod Website',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def page_non_trouvee(error):
    return render_template('erreurs/404.html', **ALAIZ_DATA), 404

@app.errorhandler(500)
def erreur_serveur(error):
    return render_template('erreurs/500.html', **ALAIZ_DATA), 500

# Context processor pour injecter les données dans tous les templates
@app.context_processor
def inject_alaiz_data():
    return dict(alaiz_data=ALAIZ_DATA)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Lancement de A Laiz Prod...")
    print(f"📍 Environnement: {os.getenv('FLASK_ENV', 'production')}")
    print(f"🔧 Debug: {debug_mode}")
    print(f"🌐 Port: {port}")
    print(f"📧 Email SMTP: {os.getenv('EMAIL_USER', 'Non configuré')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
