from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, EmailField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length
import os
from datetime import datetime
import logging

# Configuration de l'application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Configuration Email (pour formulaires de contact)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)
csrf = CSRFProtect(app)

# Formulaire de contact/devis
class ContactForm(FlaskForm):
    nom = StringField('Nom complet', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    telephone = StringField('Téléphone', validators=[DataRequired(), Length(min=8, max=20)])
    type_evenement = SelectField('Type d\'événement', choices=[
        ('', 'Sélectionnez un type'),
        ('piano-bar', 'Piano-Bar'),
        ('mariage', 'Mariage'),
        ('concert', 'Concert'),
        ('formation', 'Formation'),
        ('sono', 'A Laiz Sono'),
        ('autre', 'Autre')
    ])
    date_evenement = DateField('Date souhaitée', validators=[DataRequired()])
    message = TextAreaField('Détails de votre projet', validators=[DataRequired(), Length(min=10, max=1000)])

# Routes principales
@app.route('/')
def index():
    """Page d'accueil principale"""
    stats = {
        'experience': 15,
        'evenements': 500,
        'mariages': 200,
        'eleves': 1000,
        'publications': 12
    }
    return render_template('index.html', stats=stats)

@app.route('/services')
def services():
    """Page services détaillée"""
    services_data = [
        {
            'id': 'piano-bar',
            'nom': 'Piano-Bar',
            'icon': 'fas fa-music',
            'description': 'Ambiances musicales raffinées pour vos soirées privées, restaurants et hôtels.',
            'details': 'Répertoire varié alliant jazz, standards internationaux et musiques actuelles.',
            'duree': '2-6 heures',
            'public': 'Restaurants, hôtels, événements privés'
        },
        {
            'id': 'mariages',
            'nom': 'Mariages',
            'icon': 'fas fa-heart',
            'description': 'Célébrez votre union avec une musique sur mesure.',
            'details': 'Cérémonie, cocktail et soirée dansante personnalisés selon vos goûts.',
            'duree': 'Journée complète',
            'public': 'Couples, familles'
        },
        {
            'id': 'concerts',
            'nom': 'Concerts',
            'icon': 'fas fa-microphone',
            'description': 'Spectacles live mémorables pour tous types d\'événements.',
            'details': 'Festivals, centres culturels, événements corporatifs.',
            'duree': '45 min - 2h',
            'public': 'Grand public'
        },
        {
            'id': 'formations',
            'nom': 'Formations',
            'icon': 'fas fa-graduation-cap',
            'description': 'Cours de piano, chant et théorie musicale.',
            'details': 'Méthodes pédagogiques innovantes par Hervé Nanfang.',
            'duree': 'Cours réguliers',
            'public': 'Débutants à avancés'
        }
    ]
    return render_template('services.html', services=services_data)

@app.route('/about')
def about():
    """Page À propos du duo"""
    duo_info = {
        'flavie': {
            'nom': 'Flavie Nanfang',
            'role': 'Chanteuse Lead',
            'specialites': ['Jazz', 'Gospel', 'Variété française', 'Musiques africaines'],
            'experience': 'Plus de 15 ans sur scène',
            'description': 'Chanteuse polyvalente aux registres étendus, elle maîtrise aussi bien les standards jazz que les rythmes afro-contemporains.'
        },
        'herve': {
            'nom': 'Hervé Nanfang',
            'role': 'Pianiste & Pédagogue',
            'specialites': ['Piano classique', 'Jazz', 'Arrangement', 'Pédagogie musicale'],
            'publications': 12,
            'description': 'Pianiste de formation classique et jazz, enseignant reconnu et auteur de plusieurs ouvrages pédagogiques.'
        }
    }
    return render_template('about.html', duo=duo_info)

@app.route('/formations')
def formations():
    """Page formations détaillée"""
    formations_data = [
        {
            'nom': 'Piano Débutant',
            'duree': '3 mois',
            'niveau': 'Débutant',
            'contenu': ['Posture et technique de base', 'Lecture de partitions', 'Premiers morceaux'],
            'prix': 'Sur devis'
        },
        {
            'nom': 'Chant Individuel',
            'duree': '6 mois',
            'niveau': 'Tous niveaux',
            'contenu': ['Technique vocale', 'Interprétation', 'Répertoire varié'],
            'prix': 'Sur devis'
        },
        {
            'nom': 'Théorie Musicale',
            'duree': '4 mois',
            'niveau': 'Intermédiaire',
            'contenu': ['Harmonie', 'Analyse musicale', 'Composition'],
            'prix': 'Sur devis'
        }
    ]
    return render_template('formations.html', formations=formations_data)

@app.route('/tswefap')
def tswefap():
    """Page projet culturel Tswefap"""
    projet_info = {
        'nom': 'Projet Tswefap',
        'objectif': 'Préservation du patrimoine linguistique Batoufam',
        'description': 'Un projet culturel unique alliant tradition et innovation technologique',
        'realisations': [
            'Dictionnaire numérique Batoufam-Français',
            'Archive audio des contes traditionnels',
            'Application mobile d\'apprentissage',
            'Ateliers de transmission intergénérationnelle'
        ],
        'impact': 'Plus de 1000 locuteurs sensibilisés'
    }
    return render_template('tswefap.html', projet=projet_info)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Page contact avec formulaire de devis"""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Envoi de l'email de notification
            msg = Message(
                subject=f'Nouvelle demande de devis - {form.type_evenement.data}',
                sender=app.config['MAIL_USERNAME'],
                recipients=['contact@alaizprod.com'],  # Email de réception
                body=f"""
                Nouvelle demande de devis reçue :
                
                Nom : {form.nom.data}
                Email : {form.email.data}
                Téléphone : {form.telephone.data}
                Type d'événement : {form.type_evenement.data}
                Date souhaitée : {form.date_evenement.data}
                
                Message :
                {form.message.data}
                """
            )
            mail.send(msg)
            
            # Confirmation à l'utilisateur
            confirmation = Message(
                subject='Demande de devis reçue - A Laiz Prod',
                sender=app.config['MAIL_USERNAME'],
                recipients=[form.email.data],
                body=f"""
                Bonjour {form.nom.data},
                
                Nous avons bien reçu votre demande de devis pour votre {form.type_evenement.data}.
                
                Nous vous contacterons dans les plus brefs délais pour étudier votre projet.
                
                Cordialement,
                L'équipe A Laiz Prod
                """
            )
            mail.send(confirmation)
            
            flash('Votre demande a été envoyée avec succès ! Nous vous contacterons rapidement.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            app.logger.error(f'Erreur envoi email: {e}')
            flash('Erreur lors de l\'envoi. Veuillez réessayer ou nous contacter directement.', 'error')
    
    contact_info = {
        'phones': {
            'flavie': '+237 XXX XXX XXX',  # À remplacer par les vrais numéros
            'herve': '+237 XXX XXX XXX'
        },
        'email': 'contact@alaizprod.com',
        'address': 'Yaoundé, Cameroun',
        'social': {
            'facebook': '#',  # À remplacer par les vraies URLs
            'instagram': '#',
            'youtube': '#',
            'linkedin': '#',
            'whatsapp': '#'
        }
    }
    
    return render_template('contact.html', form=form, contact=contact_info)

# API pour les demandes AJAX
@app.route('/api/contact', methods=['POST'])
def api_contact():
    """API pour traitement AJAX du formulaire"""
    data = request.get_json()
    
    try:
        # Validation basique
        required_fields = ['nom', 'email', 'telephone', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'Le champ {field} est requis'}), 400
        
        # Traitement de la demande (ici, log simple)
        app.logger.info(f"Nouvelle demande de contact: {data['nom']} - {data['email']}")
        
        return jsonify({
            'status': 'success', 
            'message': 'Votre demande a été envoyée avec succès !'
        })
        
    except Exception as e:
        app.logger.error(f"Erreur API contact: {e}")
        return jsonify({'status': 'error', 'message': 'Erreur serveur'}), 500

# Routes d'erreur personnalisées
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Configuration de logging pour production
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = logging.FileHandler('logs/alaizprod.log')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('A Laiz Prod startup')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')
