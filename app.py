from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# Ajout des filtres Jinja2 manquants
@app.template_filter('strftime')
def strftime_filter(date, fmt='%Y-%m-%d'):
    """Filtre pour formater les dates"""
    if isinstance(date, str):
        return date
    return date.strftime(fmt) if date else ''
 Routes pour bloquer les bots WordPress/malveillants
@app.route('/wp-admin')
@app.route('/wp-admin/')
@app.route('/wp-admin/<path:path>')
@app.route('/wordpress/<path:path>')
@app.route('/wp-login.php')
@app.route('/wp-config.php')
@app.route('/admin')
@app.route('/admin/')
@app.route('/admin/<path:path>')
def block_bots(path=None):
    """Bloquer les tentatives d'accès WordPress et autres bots"""
    return '', 404

# Route pour robots.txt
@app.route('/robots.txt')
def robots_txt():
    return """User-agent: *
Disallow: /wp-admin/
Disallow: /admin/
Disallow: /wordpress/
Allow: /
""", 200, {'Content-Type': 'text/plain'}

# Configuration
app.secret_key = os.environ.get('SECRET_KEY', 'alaiz-prod-secret-key-2024')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Données du Label A Laiz Prod
label = {
    'name': 'A Laiz Prod',
    'tagline': 'Label Musical Camerounais d\'Excellence',
    'founded': '2009',
    'director': {
        'name': 'Hervé Nanfang',
        'title': 'Directeur Artistique & Fondateur',
        'phone': '+237 694 723 492',  # Remplacez par le vrai numéro
        'specialties': [
            'Piano Variétés & Jazz',
            'Composition & Arrangements',
            'Direction Artistique',
            'Pédagogie Musicale',
            'Préservation Culturelle'
        ]
    },
    'contact': {
        'email': 'contact@alaizprod.com',
        'address': 'Yaoundé, Cameroun',
        'social': {
            'facebook': 'https://facebook.com/alaizprod',
            'instagram': 'https://instagram.com/alaizprod',
            'youtube': 'https://youtube.com/@alaizprod',
            'whatsapp': 'https://wa.me/237682180266'  # Remplacez par le vrai numéro
        }
    }
}

# Services/Productions du Label
services = {
    'piano_bar': {
        'name': 'Piano-Bar Collaboratif',
        'icon': 'fas fa-piano',
        'description': 'Ambiances musicales raffinées avec rotation d\'artistes',
        'full_description': 'Hervé Nanfang au piano, accompagné de nos chanteurs et instrumentistes collaborateurs pour créer des ambiances musicales uniques qui s\'adaptent parfaitement à votre événement.',
        'packages': [
            {
                'name': 'Essentiel',
                'price': '100.000 FCFA',
                'duration': '2-4 heures',
                'includes': [
                    'Hervé Nanfang au piano',
                    '1 chanteur(se) collaborateur',
                    'Répertoire jazz & standards',
                    'Sonorisation portable'
                ]
            },
            {
                'name': 'Premium',
                'price': '320.000 FCFA',
                'duration': '4-5 heures',
                'includes': [
                    'Formation piano + 2 chanteurs',
                    'Instrumentiste en renfort',
                    'Répertoire élargi',
                    'Sonorisation professionnelle'
                ]
            }
        ]
    },
    'mariages': {
        'name': 'Créations Musicales Mariages',
        'icon': 'fas fa-heart',
        'description': 'Équipes artistiques sur mesure pour votre union',
        'full_description': 'Chaque mariage mérite une création musicale unique. Nous constituons une équipe d\'artistes personnalisée selon vos goûts, traditions et vision pour accompagner tous les moments de votre jour parfait.',
        'packages': [
            {
                'name': 'Harmonie',
                'price': '200.000 FCFA',
                'duration': 'Cérémonie + Cocktail (4h)',
                'includes': [
                    'Équipe 3-4 artistes sur mesure',
                    'Arrangements personnalisés',
                    'Cérémonie + cocktail',
                    'Consultation préparatoire'
                ]
            },
            {
                'name': 'Symphonie',
                'price': '650.000 FCFA',
                'duration': 'Journée complète (8h)',
                'includes': [
                    'Équipe 5-8 artistes modulable',
                    'Tous moments musicaux',
                    'Créations originales',
                    'Support sonorisation'
                ]
            }
        ]
    },
    'concerts': {
        'name': 'Productions Scéniques',
        'icon': 'fas fa-microphone',
        'description': 'Spectacles collaboratifs d\'exception',
        'full_description': 'Concerts et spectacles uniques rassemblant nos collaborateurs autour de créations artistiques dirigées par Hervé Nanfang, mêlant tradition camerounaise et influences internationales.',
        'packages': [
            {
                'name': 'Concert Intimiste',
                'price': '400.000 FCFA',
                'duration': '60-90 minutes',
                'includes': [
                    'Formation 3-5 artistes',
                    'Direction Hervé Nanfang',
                    'Répertoire adapté',
                    'Sound check inclus'
                ]
            },
            {
                'name': 'Spectacle Complet',
                'price': '900.000 FCFA',
                'duration': '90-120 minutes',
                'includes': [
                    'Formation 6-8 artistes',
                    'Scénographie complète',
                    'Support technique',
                    'Créations originales'
                ]
            }
        ]
    },
    'formations': {
        'name': 'Formations Musicales',
        'icon': 'fas fa-graduation-cap',
        'description': 'École d\'excellence A Laiz Prod avec méthodes Hervé Nanfang',
        'full_description': 'Formations d\'excellence basées sur 12 ouvrages pédagogiques révolutionnaires d\'Hervé Nanfang. Méthodes uniques intégrant traditions camerounaises et techniques classiques.',
        'packages': [
            {
                'name': 'Cours Particuliers',
                'price': '25.000 FCFA/mois',
                'duration': '1h/semaine',
                'includes': [
                    'Formation directe avec Hervé',
                    'Méthodes "Le petit pianiste"',
                    'Suivi personnalisé',
                    'Concert élèves annuel'
                ]
            },
            {
                'name': 'Ateliers Collectifs',
                'price': '15.000 FCFA/mois',
                'duration': '2h/semaine',
                'includes': [
                    'Petits groupes (4-6 élèves)',
                    'Apprentissage collaboratif',
                    'Esprit d\'ensemble',
                    'Projets créatifs'
                ]
            }
        ]
    },
    'sono': {
        'name': 'A Laiz Sono',
        'icon': 'fas fa-volume-up',
        'description': 'Division technique professionnelle du label',
        'full_description': 'Solutions complètes de sonorisation par la division technique A Laiz Sono. Équipements professionnels et équipe de techniciens experts pour tous vos événements.',
        'packages': [
            {
                'name': 'Pack Conférence',
                'price': '125.000 FCFA',
                'duration': 'Jusqu\'à 100 personnes',
                'includes': [
                    'Micros professionnels',
                    'Table de mixage',
                    'Enceintes monitoring',
                    'Technicien dédié'
                ]
            },
            {
                'name': 'Pack Production',
                'price': '300.000 FCFA',
                'duration': '100-300 personnes',
                'includes': [
                    'Système son complet',
                    'Éclairage LED',
                    'Régie mobile',
                    '2 techniciens + coordination'
                ]
            }
        ]
    }
}

# Collaborations et équipe
collaborations = {
    'vocalists': {
        'title': 'Chanteurs Collaborateurs',
        'icon': 'fas fa-microphone-alt',
        'count': '15+',
        'genres': ['Jazz', 'Soul', 'Gospel', 'Afro-Contemporary']
    },
    'instrumentalists': {
        'title': 'Musiciens Instrumentistes',
        'icon': 'fas fa-guitar',
        'count': '20+',
        'genres': ['Piano', 'Guitare', 'Basse', 'Batterie', 'Cuivres', 'Cordes']
    },
    'composers': {
        'title': 'Compositeurs & Arrangeurs',
        'icon': 'fas fa-pen-alt',
        'count': '8+',
        'genres': ['Composition', 'Arrangements', 'Direction musicale']
    },
    'technicians': {
        'title': 'Équipe Technique',
        'icon': 'fas fa-sliders-h',
        'count': '10+',
        'genres': ['Son', 'Éclairage', 'Vidéo', 'Régie']
    }
}

# Cours disponibles
courses = [
    {
        'name': 'Piano Variétés & Jazz',
        'level': 'Tous niveaux',
        'description': 'Formation complète basée sur les méthodes Hervé Nanfang et "Le petit pianiste"',
        'duration': '1h/semaine',
        'schedule': 'Flexible selon disponibilités',
        'price': '25.000 FCFA/mois'
    },
    {
        'name': 'Technique Vocale & Chant',
        'level': 'Débutant à Avancé',
        'description': 'Formation vocale intégrant techniques classiques et traditions africaines',
        'duration': '1h/semaine',
        'schedule': 'Matin/après-midi/soir',
        'price': '25.000 FCFA/mois'
    },
    {
        'name': 'Ateliers Collectifs',
        'level': 'Tous niveaux',
        'description': 'Apprentissage en groupe favorisant l\'esprit collaboratif A Laiz',
        'duration': '2h/semaine',
        'schedule': 'Samedi matin/après-midi',
        'price': '15.000 FCFA/mois'
    },
    {
        'name': 'Composition & Direction',
        'level': 'Intermédiaire à Pro',
        'description': 'Formation avancée vers collaboration professionnelle',
        'duration': '1h30/semaine',
        'schedule': 'Sur rendez-vous',
        'price': '35.000 FCFA/mois'
    }
]

# Statistiques du label
stats = {
    'experience': 15,
    'projects': 500,
    'collaborators': 50,
    'students': 1000,
    'publications': 12
}

# Routes principales
@app.route('/')
def index():
    try:
        return render_template('index.html', 
                             label=label, 
                             services=services, 
                             collaborations=collaborations,
                             stats=stats)
    except Exception as e:
        # Fallback si template manquant
        return f"""
        <h1>A Laiz Prod - Label Musical Camerounais</h1>
        <p>Site en cours de mise à jour...</p>
        <p>Contactez Hervé Nanfang : {label['director']['phone']}</p>
        <p>Email : {label['contact']['email']}</p>
        <p>Erreur technique : {str(e)}</p>
        """

@app.route('/about')
@app.route('/apropos')
def about():
    try:
        return render_template('about.html', 
                             label=label, 
                             collaborations=collaborations,
                             stats=stats)
    except:
        return redirect(url_for('index'))

@app.route('/services')
@app.route('/productions')
def services_page():
    try:
        return render_template('services.html', 
                             label=label, 
                             services=services,
                             stats=stats)
    except:
        return redirect(url_for('index'))

@app.route('/formations')
def formations():
    try:
        return render_template('formations.html', 
                             label=label, 
                             courses=courses,
                             stats=stats)
    except:
        return redirect(url_for('index'))

@app.route('/contact')
def contact():
    try:
        return render_template('contact.html', 
                             label=label,
                             services=services)
    except:
        return redirect(url_for('index'))

# Routes API pour données dynamiques
@app.route('/api/stats')
def api_stats():
    return jsonify(stats)

@app.route('/api/collaborations')
def api_collaborations():
    return jsonify(collaborations)

@app.route('/api/services')
def api_services():
    return jsonify(services)

# Route pour traitement formulaire contact
@app.route('/contact', methods=['POST'])
def contact_form():
    try:
        # Récupération des données du formulaire
        request_type = request.form.get('request_type')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        project_description = request.form.get('project_description')
        
        # Validation basique
        if not all([request_type, full_name, email, phone]):
            flash('Tous les champs obligatoires doivent être remplis.', 'error')
            return redirect(url_for('contact'))
        
        # Ici, vous ajouteriez la logique pour traiter le formulaire
        # (envoi email, sauvegarde base de données, etc.)
        
        flash('Votre demande a été envoyée avec succès ! Nous vous contacterons dans les 24h.', 'success')
        return redirect(url_for('contact'))
        
    except Exception as e:
        flash('Une erreur s\'est produite. Veuillez réessayer.', 'error')
        return redirect(url_for('contact'))

# Gestion des erreurs
@app.errorhandler(404)
def not_found(error):
    return render_template_string("""
    <h1>Page non trouvée</h1>
    <p>La page demandée n'existe pas.</p>
    <a href="{{ url_for('index') }}">Retour à l'accueil</a>
    """), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template_string("""
    <h1>Erreur interne</h1>
    <p>Une erreur s'est produite sur le serveur.</p>
    <a href="{{ url_for('index') }}">Retour à l'accueil</a>
    """), 500

# Test de santé pour le déploiement
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'OK',
        'label': label['name'],
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

# Configuration pour le déploiement
if __name__ == '__main__':
    # Configuration pour développement local
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
else:
    # Configuration pour production (Gunicorn)
    application = app

