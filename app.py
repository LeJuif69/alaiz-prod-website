from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'alaiz-prod-2010-herve-nanfang')

# DONNÉES COMPLÈTES A LAIZ PROD
ALAIZ_DATA = {
    "nom": "A Laiz Prod",
    "slogan": "Tradition. Innovation. Émotion.",
    "directeur": "Hervé Nanfang",
    "telephones": ["+237 694 723 492", "+237 682 180 266"],
    "emails": {
        "contact": "contact@alaizopays.art",
        "booking": "booking@alaizopays.art", 
        "formation": "formation@alaizopays.art"
    },
    "adresse": "Rue Nachtigall, Melen, Yaoundé – Cameroun",
    "annee_fondation": 2010,
    
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
    
    # Section Blog - Articles d'exemple
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
    
    "categories_blog": ["Actus du Label", "Portrait d'Artiste", "Formations", "Événements", "Culture & Innovation"],
    
    # Instruments
    "instruments": [
        "Yamaha Genos", "Yamaha Tyros", "Roland Fantom", "Korg PA5X",
        "Yamaha SX900", "Yamaha SX600", "Sonorisation professionnelle", "Éclairage scénique"
    ],
    
    # Réseaux sociaux
    "reseaux_sociaux": {
        "facebook": "https://facebook.com/alaizprodcameroun",
        "instagram": "https://instagram.com/alaizprod_officiel", 
        "youtube": "https://youtube.com/@alaizprod",
        "whatsapp": "https://wa.me/237694723492"
    }
}

@app.route('/')
def accueil():
    annee_courante = datetime.now().year
    annees_experience = annee_courante - ALAIZ_DATA["annee_fondation"]
    
    context = {
        **ALAIZ_DATA,
        "annees_experience": annees_experience,
        "annee_courante": annee_courante
    }
    return render_template('index.html', **context)

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        try:
            nom = request.form.get('nom')
            email = request.form.get('email')
            telephone = request.form.get('telephone')
            service = request.form.get('service')
            message = request.form.get('message')
            
            if not nom or not email or not message:
                return jsonify({
                    'success': False, 
                    'message': 'Le nom, l\'email et le message sont obligatoires.'
                })
            
            envoyer_email_contact(nom, email, telephone, service, message)
            
            return jsonify({
                'success': True, 
                'message': 'Merci pour votre message ! Hervé vous contactera rapidement.'
            })
            
        except Exception as e:
            return jsonify({
                'success': False, 
                'message': 'Une erreur s\'est produite. Contactez-nous directement par téléphone.'
            })

def envoyer_email_contact(nom, email, telephone, service, message):
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    if not all([smtp_server, smtp_username, smtp_password]):
        return
    
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = ALAIZ_DATA["emails"]["contact"]
    msg['Subject'] = f'Nouveau message A Laiz Prod - {service}'
    
    corps_message = f"""
    NOUVEAU MESSAGE - A LAIZ PROD
    =============================
    
    Nom: {nom}
    Email: {email}
    Téléphone: {telephone or 'Non renseigné'}
    Service: {service or 'Non spécifié'}
    
    Message:
    {message}
    
    ---
    Envoyé le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
    """
    
    msg.attach(MIMEText(corps_message, 'plain'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
