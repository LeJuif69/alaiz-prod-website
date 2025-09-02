import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, make_response
from flask_mail import Mail, Message

# ==============================================
# CONFIGURATION DE BASE
# ==============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'alaiz-prod-secret-key-2024')

# Logging configuré
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration email
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'votre_email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS', 'votre_mot_de_passe')

mail = Mail(app)

# ==============================================
# DONNÉES DU LABEL MUSICAL A LAIZ PROD
# ==============================================

LABEL_INFO = {
    'name': 'A Laiz Prod',
    'tagline': 'Label Musical Camerounais',
    'description': "Plateforme de créations artistiques et collaborations musicales d'excellence",
    'founded': 2009,
    'location': 'Yaoundé, Cameroun',
    'vision': "Révéler et fédérer les talents camerounais et internationaux autour de créations musicales d'exception",
    'director': {
        'name': 'Hervé Nanfang',
        'title': 'Fondateur & Directeur Artistique',
        'bio': "Pianiste de formation classique et jazz, pédagogue reconnu et visionnaire culturel.",
        'specialties': [
            'Direction Artistique',
            'Piano Classique & Jazz',
            'Pédagogie Musicale',
            'Arrangements & Compositions',
            'Projet Culturel Tswefap',
            'Collaborations Internationales'
        ],
        'phone': os.environ.get('DIRECTOR_PHONE', '+237 XXX XXX XXX'),
        'email': os.environ.get('DIRECTOR_EMAIL', 'herve@alaizprod.com')
    },
    'contact': {
        'main_phone': os.environ.get('DIRECTOR_PHONE', '+237 XXX XXX XXX'),
        'email': os.environ.get('CONTACT_EMAIL', 'contact@alaizprod.com'),
        'booking_email': os.environ.get('BOOKING_EMAIL', 'booking@alaizprod.com'),
        'address': 'Yaoundé, Cameroun',
        'social': {
            'facebook': os.environ.get('FACEBOOK_URL', 'https://facebook.com/alaizprod'),
            'instagram': os.environ.get('INSTAGRAM_URL', 'https://instagram.com/alaizprod'),
            'youtube': os.environ.get('YOUTUBE_URL', 'https://youtube.com/alaizprod'),
            'linkedin': os.environ.get('LINKEDIN_URL', 'https://linkedin.com/in/hervenanfang'),
            'whatsapp': os.environ.get('WHATSAPP_URL', 'https://wa.me/237XXXXXXXXX')
        }
    }
}

LABEL_STATS = {
    'experience': datetime.now().year - LABEL_INFO['founded'],
    'projects': 500,
    'collaborators': 50,
    'students': 1000,
    'publications': 12
}

# ==============================================
# INTERCEPTER HEAD POUR ÉVITER LES 502
# ==============================================

@app.before_request
def handle_head():
    if request.method == 'HEAD':
        return make_response('', 200)

# ==============================================
# ROUTES PRINCIPALES
# ==============================================

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return render_template('index.html',
                           label=LABEL_INFO,
                           services={},  # ⚠️ mettre tes SERVICES_DATA ici si tu veux
                           collaborations={},
                           stats=LABEL_STATS)

@app.route('/about', methods=['GET', 'HEAD'])
def about():
    return render_template('about.html', label=LABEL_INFO)

@app.route('/services', methods=['GET', 'HEAD'])
def services():
    return render_template('services.html', label=LABEL_INFO)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        message = request.form.get('message', '').strip()

        if not all([name, email, phone]):
            flash("Nom, email et téléphone sont obligatoires.", "error")
            return render_template('contact.html', label=LABEL_INFO)

        try:
            subject = f"Nouvelle demande - A Laiz Prod"
            email_body = f"Client: {name}\nEmail: {email}\nTel: {phone}\n\nMessage:\n{message}"

            msg = Message(subject=subject,
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[LABEL_INFO['contact']['email']],
                          body=email_body)

            mail.send(msg)
            flash("Votre demande a été envoyée avec succès !", "success")
        except Exception as e:
            logger.error("Erreur envoi email", exc_info=True)
            flash("Une erreur est survenue lors de l’envoi de votre demande.", "error")

        return redirect(url_for('contact'))

    return render_template('contact.html', label=LABEL_INFO)

# ==============================================
# API
# ==============================================

@app.route('/api/stats')
def api_stats():
    return jsonify(LABEL_STATS)

# ==============================================
# ERREURS
# ==============================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', label=LABEL_INFO), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error("Erreur interne", exc_info=True)
    return render_template('500.html', label=LABEL_INFO), 500

# ==============================================
# LANCEMENT
# ==============================================

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
