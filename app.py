from flask import Flask, render_template, request, flash, redirect, url_for, Response
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Importations pour formulaires sécurisés
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# --- FORMULAIRE CONTACT SÉCURISÉ ---
class ContactForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telephone = StringField('Téléphone (Optionnel)')
    service = SelectField('Service Concerné',
                          choices=[
                              ('prestation', 'Prestation musicale'),
                              ('location', 'Location d\'instruments'),
                              ('formation', 'Formation musicale'),
                              ('production', 'Production musicale'),
                              ('autre', 'Autre')
                          ],
                          validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Envoyer le Message')

# --- DONNÉES CENTRALISÉES A LAIZ PROD ---
ALAIZ_DATA = {
    "nom": "A Laiz Prod",
    "slogan": "Tradition. Innovation. Émotion.",
    "directeur": "Hervé Nanfang",
    "telephones": ["+237 694 723 492", "+237 682 180 266"],
    "email_contact": "contact@alaizopays.art",
    "email_booking": "booking@alaizopays.art",
    "email_formation": "formation@alaizopays.art",
    "adresse": "Rue Nachtigall, Melen, Yaoundé, Cameroun",
    "annee_fondation": 2010,
    
    # 🎨 IDENTITÉ VISUELLE DYNAMIQUE CENTRALISÉE
    "BRAND_STYLE": {
        # Couleurs principales
        "alaiz_gold": "#D4AF37",
        "alaiz_gold_light": "#E8C766", 
        "alaiz_black": "#0A0A0A",
        "alaiz_earth": "#8B4513",
        "alaiz_terracotta": "#A0522D",
        "alaiz_white": "#FFFFFF",
        "alaiz_cream": "#F8F4E9",
        "alaiz_gray": "#2A2A2A",
        
        # Typographie
        "font_heading": "'Playfair Display', serif",
        "font_subheading": "'Montserrat', sans-serif", 
        "font_body": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        
        # Espacements et rayons
        "space_xs": "0.25rem",
        "space_sm": "0.5rem",
        "space_md": "1rem",
        "space_lg": "2rem", 
        "space_xl": "3rem",
        "radius_sm": "4px",
        "radius_md": "8px",
        "radius_lg": "12px"
    },
    
    "specialites": [
        "Production musicale & direction artistique",
        "Événementiel musical (concerts, mariages, institutionnel)",
        "Location d'instruments et matériel technique",
        "Concept Piano-Bar A Laiz"
    ],
    
    "instruments": [
        "Yamaha Genos", "Tyros", "Roland Fantom", "Korg PA5X", 
        "Yamaha SX900", "SX600", "Sonorisation et lumière"
    ],
    
    "artistes_phares": [
        "Aladji Touré", "Étienne Bappé", "Kares Fotso", "Lady Ponce",
        "Richard Amougou", "Tala André Marie", "Stypak Samo", "Angélique Kidjo",
        "Sagbohan Danialou", "Rikos Campos", "Toofan", "Big Caïd"
    ],
    
    "realisations": [
        "Album Shepo (2013) + nouvel album en préparation",
        "Bafoussam Worship Experience (30 novembre 2025)",
        "Inauguration de MikeLand (Bénin)",
        "Première partie d'Asalfo (Magic System)",
        "Première partie de Diam's (2010)",
        "CAFRIM 2013 - Trophée du Meilleur Compositeur Tradi-Moderne"
    ],
    
    "formations": [
        "Chant et technique vocale",
        "Piano et claviers arrangeurs",
        "Technique de scène",
        "Composition musicale",
        "MAO (Musique Assistée par Ordinateur)",
        "Musicologie appliquée aux médias visuels",
        "Histoire de l'art musical"
    ],
    
    "reseaux_sociaux": {
        "facebook": "https://facebook.com/alaizprodcameroun",
        "instagram": "https://instagram.com/alaizprod_officiel", 
        "youtube": "https://youtube.com/@alaizprod",
        "whatsapp": "https://wa.me/237694723492"
    }
}

# --- CONTEXTE GLOBAL POUR TEMPLATES ---
@app.context_processor
def inject_global_context():
    annee_courante = datetime.now().year
    annees_experience = annee_courante - ALAIZ_DATA["annee_fondation"]
    
    return {
        'site_data': ALAIZ_DATA,
        'brand_style': ALAIZ_DATA["BRAND_STYLE"],
        'annees_experience': annees_experience,
        'annee_courante': annee_courante
    }

# --- ROUTE POUR CSS DYNAMIQUE ---
@app.route('/dynamic_styles.css')
def dynamic_styles():
    """Génère le CSS avec les variables de style injectées"""
    css_content = render_template('css/alaiz_styles.jinja', 
                                brand=ALAIZ_DATA["BRAND_STYLE"])
    return Response(css_content, mimetype='text/css')

# --- ROUTES PRINCIPALES ---
@app.route('/')
def accueil():
    contact_form = ContactForm()
    return render_template('index.html', form=contact_form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            nom = form.nom.data
            email = form.email.data
            telephone = form.telephone.data
            service_label = dict(form.service.choices).get(form.service.data)
            message = form.message.data
            
            envoyer_email_contact(nom, email, telephone, service_label, message)
            flash('Merci pour votre message ! Nous vous contacterons rapidement.', 'success')
            
        except Exception as e:
            print(f"Erreur envoi email : {e}")
            flash("Une erreur s'est produite. Contactez-nous directement.", 'danger')
        
        return redirect(url_for('accueil') + '#contact-section')
    
    # Si erreurs de validation
    if form.errors:
        flash('Veuillez corriger les erreurs dans le formulaire.', 'danger')
    
    return render_template('index.html', form=form)

# --- FONCTION ENVOI EMAIL ---
def envoyer_email_contact(nom, email, telephone, service, message):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    if not all([smtp_server, smtp_username, smtp_password]):
        raise Exception("Configuration SMTP manquante dans .env")
    
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
    """
    
    msg.attach(MIMEText(corps_message, 'plain'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

# --- LANCEMENT SERVEUR ---
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
