from flask import Flask, render_template, request, flash, redirect, url_for
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Importations nécessaires pour les formulaires sécurisés
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# Charger les variables d'environnement depuis le fichier.env
load_dotenv()

app = Flask(__name__)
# La clé secrète est maintenant lue depuis le fichier.env, c'est plus sécurisé
app.config = os.environ.get('SECRET_KEY')

# --- DÉFINITION DU FORMULAIRE DE CONTACT SÉCURISÉ AVEC FLASK-WTF ---
# Cette classe définit les champs du formulaire et leurs règles de validation.
class ContactForm(FlaskForm):
    nom = StringField('Nom', validators=)
    email = StringField('Email', validators=)
    telephone = StringField('Téléphone (Optionnel)')
    # Les 'choices' sont les options qui apparaîtront dans le menu déroulant du formulaire
    service = SelectField('Service Concerné', choices=, validators=)
    message = TextAreaField('Message', validators=)
    submit = SubmitField('Envoyer le Message')

# --- DONNÉES DU LABEL (VOTRE STRUCTURE ORIGINALE CONSERVÉE ET AMÉLIORÉE) ---
# On garde votre dictionnaire qui est la base de tout le contenu du site.
# On remplace juste les valeurs de contact par celles du fichier.env.
ALAIZ_DATA = {
    "nom": os.environ.get('LABEL_NAME'),
    "slogan": "Tradition. Innovation. Émotion.",
    "directeur": os.environ.get('DIRECTOR_NAME'),
    # On reconstruit la liste des téléphones à partir du.env
    "telephones":,
    "email_contact": os.environ.get('CONTACT_EMAIL'),
    "adresse": os.environ.get('ADDRESS'),
    "annee_fondation": 2010,
    
    # TOUTES VOS DONNÉES DE CONTENU SONT CONSERVÉES ICI
    "specialites":,
    "instruments":,
    "artistes_phares":,
    "realisations":,
    "formations":,
    "categories_blog": [
        "Événements", "Formation", "Musique & Culture", "Conseils pour artistes"
    ],
    "reseaux_sociaux": {
        "facebook": os.environ.get('SOCIAL_FACEBOOK_URL'),
        "instagram": os.environ.get('SOCIAL_INSTAGRAM_URL'),
        "youtube": os.environ.get('SOCIAL_YOUTUBE_URL'),
        "whatsapp": os.environ.get('SOCIAL_WHATSAPP_URL')
    }
}

# --- CONTEXTE GLOBAL POUR LES TEMPLATES ---
# Cette fonction rend automatiquement les variables de style et les données du label
# disponibles sur TOUTES les pages, sans avoir à les passer manuellement dans chaque route.
@app.context_processor
def inject_global_context():
    annee_courante = datetime.now().year
    annees_experience = annee_courante - ALAIZ_DATA["annee_fondation"]
    
    return {
        'primary_color': os.environ.get('PRIMARY_COLOR'),
        'secondary_color': os.environ.get('SECONDARY_COLOR'),
        'accent_color': os.environ.get('ACCENT_COLOR'),
        'font_headings': os.environ.get('FONT_HEADINGS'),
        'font_body': os.environ.get('FONT_BODY'),
        'site_data': ALAIZ_DATA,
        'annees_experience': annees_experience,
        'annee_courante': annee_courante
    }

# --- ROUTES DE L'APPLICATION ---
@app.route('/')
def accueil():
    # On crée une instance du formulaire pour pouvoir l'afficher dans le template
    contact_form = ContactForm()
    return render_template('index.html', form=contact_form)

# Route dédiée au traitement du formulaire, plus propre et sécurisée
@app.route('/contact', methods=)
def contact():
    form = ContactForm()
    # form.validate_on_submit() fait tout le travail :
    # 1. Vérifie si la requête est POST.
    # 2. Vérifie que le jeton de sécurité CSRF est valide.
    # 3. Vérifie que toutes les règles de validation (DataRequired, Email, etc.) sont respectées.
    if form.validate_on_submit():
        try:
            # On récupère les données validées et nettoyées
            nom = form.nom.data
            email = form.email.data
            telephone = form.telephone.data
            service_label = dict(form.service.choices).get(form.service.data)
            message = form.message.data
            
            envoyer_email_contact(nom, email, telephone, service_label, message)
            
            # On envoie un message de succès à l'utilisateur
            flash('Merci pour votre message! Nous vous contacterons rapidement.', 'success')
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")
            flash("Une erreur s'est produite. Veuillez nous contacter directement par téléphone.", 'danger')
        
        # On redirige l'utilisateur vers la page d'accueil, au niveau de la section contact
        return redirect(url_for('accueil') + '#contact-section')

    # Si le formulaire n'est pas valide, on recharge la page d'accueil.
    # Flask-WTF va automatiquement passer les messages d'erreur au template.
    flash('Le formulaire contient des erreurs. Veuillez vérifier les champs en rouge.', 'danger')
    return render_template('index.html', form=form)


def envoyer_email_contact(nom, email, telephone, service, message):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    if not all([smtp_server, smtp_username, smtp_password]):
        print("ERREUR: Variables SMTP non configurées dans le fichier.env")
        raise Exception("Configuration SMTP manquante")
    
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg = ALAIZ_DATA["email_contact"]
    msg = f'Nouveau message A Laiz Prod - {service}'
    
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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
