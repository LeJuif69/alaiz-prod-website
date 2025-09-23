from flask import Flask, render_template, request, flash, redirect, url_for
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Importations pour les formulaires sécurisés
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# Charger les variables d'environnement depuis le fichier.env
load_dotenv()

app = Flask(__name__)
# La clé secrète est maintenant lue depuis le fichier.env, c'est plus sécurisé
app.config = os.environ.get('SECRET_KEY')

# DONNÉES RÉELLES A LAIZ PROD
ALAIZ_DATA = {
    "nom": "A Laiz Prod",
    "slogan": "Tradition. Innovation. Émotion.",
    "directeur": "Hervé Nanfang",
    "telephones": ["+237 694 723 492", "+237 682 180 266"],
    "email_contact": "contact@alaizopays.art",
    "adresse": "Yaoundé, Cameroun",
    "annee_fondation": 2010,
    
    # Spécialités
    "specialites": [
        "Production musicale & direction artistique",
        "Événementiel musical (concerts, mariages, institutionnel)",
        "Location d'instruments et matériel technique",
        "Concept Piano-Bar A Laiz"
    ],
    
    # Instruments disponibles
    "instruments": [
        "Yamaha Genos", "Tyros", "Roland Fantom", "Korg PA5X", 
        "Yamaha SX900", "SX600", "Sonorisation et lumière"
    ],
    
    # Artistes et collaborations
    "artistes_phares": [
        "Aladji Touré", "Étienne Bappé", "Kares Fotso", "Lady Ponce",
        "Richard Amougou", "Tala André Marie", "Stypak Samo", "Angélique Kidjo",
        "Sagbohan Danialou", "Rikos Campos", "Toofan", "Big Caïd"
    ],
    
    # Réalisations marquantes
    "realisations": [
        "Album Shepo (2013) + nouvel album en préparation",
        "Bafoussam Worship Experience (30 novembre 2025)",
        "Inauguration de MikeLand (Bénin)",
        "Première partie d'Asalfo (Magic System)",
        "Première partie de Diam's (2010)",
        "Yafé (Yaoundé en Fête, 2012)",
        "PROMOTE, Écrans Noirs",
        "Africa Star Dakar 2010",
        "Stars 2 Demain (Cameroun, Dakar, Abidjan)",
        "Coupe d'Afrique de Musique CAFRIM 2013 - Trophée du Meilleur Compositeur Tradi-Moderne"
    ],
    
    # Pédagogie
    "formations": [
        "Chant et technique vocale",
        "Piano et claviers",
        "Technique de scène",
        "Composition musicale",
        "MAO (Musique Assistée par Ordinateur)",
        "Musicologie appliquée aux médias visuels",
        "Histoire de l'art"
    ],
    
    # Blog
    "categories_blog": [
        "Événements", "Formation", "Musique & Culture", "Conseils pour artistes"
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
            
            # Envoi d'email
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
    """Fonction pour envoyer les emails de contact"""
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    if not all([smtp_server, smtp_username, smtp_password]):
        return
    
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = ALAIZ_DATA["email_contact"]
    msg['Subject'] = f'Nouveau message A Laiz Prod - {service}'
    
    corps_message = f"""
    NOUVEAU MESSAGE - A LAIZ PROD
    =============================
    
    De: {nom}
    Email: {email}
    Téléphone: {telephone or 'Non renseigné'}
    Service: {service or 'Non spécifié'}
    
    Message:
    {message}
    
    ---
    Envoyé le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
    Site: https://alaizopays.art
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

