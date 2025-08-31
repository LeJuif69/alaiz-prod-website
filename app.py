rom flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_mail import Mail, Message  # Pour les emails de contact
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete_ici'

# Configuration email (optionnel pour le formulaire de contact)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'votre_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'votre_mot_de_passe'

mail = Mail(app)

# ROUTES PRINCIPALES
@app.route('/')
def index():
    """Page d'accueil avec design premium"""
    return render_template('index.html')

@app.route('/services')
def services():
    """Page services détaillée"""
    services_data = {
        'piano_bar': {
            'title': 'Piano-Bar',
            'description': 'Ambiances musicales raffinées...',
            'packages': [
                {'name': 'Mini', 'price': '50.000 FCFA', 'duration': '2h'},
                {'name': 'Standard', 'price': '75.000 FCFA', 'duration': '3h'},
                {'name': 'Premium', 'price': '100.000 FCFA', 'duration': '4h'}
            ]
        },
        'mariages': {
            'title': 'Mariages',
            'description': 'Célébrez votre union...',
            'packages': [
                {'name': 'Essentiel', 'price': 'Sur devis', 'includes': ['Cérémonie', 'Cocktail']},
                {'name': 'Complet', 'price': 'Sur devis', 'includes': ['Cérémonie', 'Cocktail', 'Soirée']}
            ]
        }
        # Ajouter autres services...
    }
    return render_template('services.html', services=services_data)

@app.route('/about')
def about():
    """Page à propos détaillée"""
    team_info = {
        'flavie': {
            'name': 'Flavie Nanfang',
            'role': 'Chanteuse professionnelle',
            'bio': 'Chanteuse polyvalente aux registres étendus...',
            'specialties': ['Jazz', 'Afro-contemporain', 'Gospel']
        },
        'herve': {
            'name': 'Hervé Nanfang',
            'role': 'Pianiste & Pédagogue',
            'bio': 'Pianiste de formation classique et jazz...',
            'specialties': ['Piano classique', 'Jazz', 'Pédagogie']
        }
    }
    return render_template('about.html', team=team_info)

@app.route('/formations')
def formations():
    """Page formations détaillée"""
    courses = [
        {
            'name': 'Piano Débutant',
            'duration': '3 mois',
            'price': '25.000 FCFA/mois',
            'schedule': 'Mer/Sam 14h-16h'
        },
        {
            'name': 'Chant Professionnel',
            'duration': '6 mois',
            'price': '30.000 FCFA/mois',
            'schedule': 'Mar/Jeu 16h-18h'
        }
        # Ajouter autres formations...
    ]
    return render_template('formations.html', courses=courses)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Page contact avec formulaire fonctionnel"""
    if request.method == 'POST':
        # Traitement du formulaire
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        event_type = request.form.get('event_type')
        event_date = request.form.get('event_date')
        message = request.form.get('message')
        
        # Validation basique
        if not all([name, email, phone]):
            flash('Veuillez remplir tous les champs obligatoires', 'error')
            return redirect(url_for('contact'))
        
        # Envoi email (optionnel)
        try:
            msg = Message(
                subject=f'Nouvelle demande de devis - {event_type}',
                sender=app.config['MAIL_USERNAME'],
                recipients=['contact@alaizprod.com'],  # Votre email
                body=f"""
                Nouvelle demande de devis :
                
                Nom: {name}
                Email: {email}
                Téléphone: {phone}
                Type d'événement: {event_type}
                Date souhaitée: {event_date}
                Message: {message}
                """
            )
            mail.send(msg)
            flash('Votre demande a été envoyée avec succès !', 'success')
        except:
            flash('Demande reçue ! Nous vous contacterons bientôt.', 'success')
        
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

if __name__ == '__main__':
    app.run(debug=True)
