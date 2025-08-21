from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'alaiz-prod-secret-key-2025')

# ============================================================================
# ROUTES PRINCIPALES - CORRIGÉES POUR UTILISER DES TEMPLATES SÉPARÉS
# ============================================================================

@app.route("/")
def home():
    """Page d'accueil - Utilise index.html"""
    return render_template("index.html", page="accueil")

@app.route("/about")
def about():
    """Page À propos - Utilise about.html"""
    try:
        return render_template("about.html", page="about")
    except:
        # Fallback si about.html n'existe pas encore
        return render_template("index.html", page="about")

@app.route("/services")
def services():
    """Page Services - Utilise services.html"""
    try:
        return render_template("services.html", page="services")
    except:
        # Fallback si services.html n'existe pas encore
        return render_template("index.html", page="services")

@app.route("/formations")
def formations():
    """Page Formations - Utilise formations.html"""
    try:
        return render_template("formations.html", page="formations")
    except:
        # Fallback si formations.html n'existe pas encore
        return render_template("index.html", page="formations")

@app.route("/contact")
def contact():
    """Page Contact - Utilise contact.html"""
    try:
        return render_template("contact.html", page="contact")
    except:
        # Fallback si contact.html n'existe pas encore
        return render_template("index.html", page="contact")

@app.route("/boutique")
def boutique():
    """Page Boutique - Utilise boutique.html ou fallback vers index.html"""
    try:
        return render_template("boutique.html", page="boutique")
    except:
        # Fallback si boutique.html n'existe pas encore
        return render_template("index.html", page="boutique")

@app.route("/label")
def label():
    """Page Label - Fallback vers index.html pour l'instant"""
    return render_template("index.html", page="label")

@app.route("/artiste")
def artiste():
    """Page Artiste - Fallback vers index.html pour l'instant"""
    return render_template("index.html", page="artiste")

# Route de test pour vérifier le routage
@app.route("/test")
def test_route():
    """Route de test pour vérifier que le routage fonctionne"""
    return """
    <div style="padding: 4rem; text-align: center; background: linear-gradient(135deg, #4f46e5, #8b5cf6); color: white; font-family: Arial;">
        <h1 style="color: #f59e0b; font-size: 3rem; margin-bottom: 1rem;">✅ ROUTAGE CORRIGÉ !</h1>
        <p style="font-size: 1.2rem; margin-bottom: 2rem;">Le nouveau app.py fonctionne parfaitement ! 🎉</p>
        
        <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; margin: 2rem auto; max-width: 600px;">
            <h3 style="color: #f59e0b; margin-bottom: 1rem;">Tests des Routes :</h3>
            <ul style="list-style: none; padding: 0;">
                <li style="margin: 0.5rem 0;"><a href="/" style="color: white; text-decoration: none;">🏠 Accueil</a></li>
                <li style="margin: 0.5rem 0;"><a href="/about" style="color: white; text-decoration: none;">👥 À Propos</a></li>
                <li style="margin: 0.5rem 0;"><a href="/services" style="color: white; text-decoration: none;">🎵 Services</a></li>
                <li style="margin: 0.5rem 0;"><a href="/formations" style="color: white; text-decoration: none;">🎓 Formations</a></li>
                <li style="margin: 0.5rem 0;"><a href="/contact" style="color: white; text-decoration: none;">📞 Contact</a></li>
            </ul>
        </div>
        
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Chaque page utilise maintenant son propre template !<br>
            A LAIZ PROD - Les Nanfang - Cameroun 🇨🇲
        </p>
    </div>
    """

# ============================================================================
# API ROUTES - SIMPLIFIÉES
# ============================================================================

@app.route("/api/weather")
def api_weather():
    """API pour les données météo simulées"""
    weather_data = {
        "temperature": 24,
        "condition": "Partiellement nuageux",
        "icon": "🌤️",
        "city": "Yaoundé",
        "humidity": 72,
        "wind": "8 km/h"
    }
    return jsonify(weather_data)

@app.route("/api/ai-chat", methods=["POST"])
def ai_chat():
    """API pour le chat IA - Version simplifiée"""
    try:
        data = request.get_json()
        message = data.get('message', '').lower()
        
        # Réponses IA personnalisées A LAIZ PROD
        responses = {
            'bonjour': 'Bonjour ! Je suis l\'assistant IA d\'A LAIZ PROD. Comment puis-je vous aider aujourd\'hui ? 🎵',
            'services': 'Nous proposons : Piano-bar (100-200K FCFA), Mariages (250K FCFA), Formations piano/chant (12-15K FCFA/cours). Que vous intéresse ?',
            'prix': 'Nos tarifs : Piano-bar 100-200K, Mariages 250K, Formations 12-15K/cours. Contactez +237 694723492 pour un devis express !',
            'formation': 'Cours avec Hervé Nanfang (piano) et Flavie Nanfang (chant). Méthode personnalisée, première consultation gratuite !',
            'contact': '📞 Tel: +237 682180266 | 💬 WhatsApp: +237 694723492 | 📧 contact@alaizopays.art',
            'mariage': 'Pack Mariage Complet 250K FCFA : Cérémonie + Réception + Piano-voix. Prestation sur-mesure !',
            'piano': 'Cours piano avec Hervé Nanfang : 15K FCFA/cours, méthode classique et jazz. Forfait 8 cours : 90K FCFA.',
            'chant': 'Cours chant avec Flavie Nanfang : 12K FCFA/cours, technique vocale avancée. Forfait 4 cours : 40K FCFA.',
            'nanfang': 'Flavie (chanteuse) et Hervé (pianiste) Nanfang forment le duo A LAIZ PROD, basé à Yaoundé. Plus de 10 ans d\'expérience !',
            'cameroun': 'A LAIZ PROD est basé à Yaoundé, Cameroun. Nous nous déplaçons dans toute la région Centre et au-delà.',
        }
        
        # Recherche de mots-clés
        for keyword, response in responses.items():
            if keyword in message:
                return jsonify({
                    'response': response,
                    'source': 'ai',
                    'timestamp': datetime.now().isoformat()
                })
        
        # Réponse par défaut
        return jsonify({
            'response': 'Merci pour votre message ! Pour une réponse personnalisée, contactez-nous au +237 694723492 (WhatsApp) ou +237 682180266. 🎵',
            'source': 'fallback',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'response': 'Désolé, je rencontre un problème technique. Contactez-nous directement au +237 694723492 !',
            'source': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route("/api/smart-form", methods=["POST"])
def smart_form():
    """API pour l'analyse IA du formulaire"""
    try:
        data = request.get_json()
        description = data.get('description', '').lower()
        
        suggestions = []
        
        if 'mariage' in description:
            suggestions.extend([
                '💍 Pack Mariage Complet - 250 000 FCFA',
                '🎵 Piano-bar Standard - 150 000 FCFA',
                '💒 Cérémonie musicale - 100 000 FCFA'
            ])
        
        if 'formation' in description or 'cours' in description:
            suggestions.extend([
                '🎓 Cours Piano Hervé Nanfang - 15 000 FCFA/cours',
                '🎤 Cours Chant Flavie Nanfang - 12 000 FCFA/cours',
                '🎹 Stage intensif week-end - 45 000 FCFA'
            ])
        
        if 'concert' in description or 'orchestre' in description:
            suggestions.extend([
                '🎤 Orchestre Prestige - 500 000 FCFA',
                '🔊 Sonorisation premium - 160 000 FCFA',
                '🎥 Prestation complète - Devis sur mesure'
            ])
        
        if 'sono' in description or 'sonorisation' in description:
            suggestions.extend([
                '🔊 Sono légère - 50 000 FCFA',
                '🎚️ Sono standard - 100 000 FCFA',
                '🎛️ Sono premium - 160 000 FCFA'
            ])
        
        if not suggestions:
            suggestions = [
                '🎯 Consultation personnalisée gratuite',
                '📞 Entretien avec Les Nanfang',
                '💡 Analyse de vos besoins spécifiques',
                '🎵 Devis sur-mesure adapté à votre budget'
            ]
        
        return jsonify({
            'suggestions': suggestions,
            'analysis': 'Analyse IA terminée - A LAIZ PROD',
            'confidence': 95,
            'contact': '+237 694723492 (WhatsApp Express)'
        })
        
    except Exception as e:
        return jsonify({
            'suggestions': ['🎯 Consultation personnalisée recommandée - Contactez +237 694723492'],
            'error': 'Erreur d\'analyse'
        }), 500

@app.route("/api/contact", methods=["POST"])
def submit_contact():
    """API pour soumission du formulaire de contact"""
    try:
        data = request.get_json()
        
        # Simulation de sauvegarde (sans base de données pour l'instant)
        contact_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'project': data.get('project'),
            'timestamp': datetime.now().isoformat(),
            'status': 'received',
            'reference': f'ALAIZ-{datetime.now().strftime("%Y%m%d%H%M%S")}'
        }
        
        # Log pour debugging (visible dans les logs Render)
        print(f"📧 Nouveau contact reçu: {contact_data['name']} - {contact_data['email']}")
        
        return jsonify({
            'success': True,
            'message': 'Votre demande a été reçue ! Nous vous contacterons sous 24h.',
            'reference': contact_data['reference'],
            'whatsapp': '+237 694723492',
            'phone': '+237 682180266'
        })
        
    except Exception as e:
        print(f"❌ Erreur API contact: {e}")
        return jsonify({
            'success': False,
            'message': 'Erreur lors de l\'envoi. Contactez-nous directement au +237 694723492',
            'whatsapp': '+237 694723492'
        }), 500

@app.route("/api/performance")
def api_performance():
    """API pour les métriques de performance"""
    import random
    
    return jsonify({
        'fps': random.randint(55, 60),
        'latency': random.randint(8, 15),
        'memory': random.randint(45, 65),
        'cpu': random.randint(20, 40),
        'status': 'A LAIZ PROD - Optimisé'
    })

# ============================================================================
# GESTION DES ERREURS
# ============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """Page 404 personnalisée"""
    return """
    <div style="padding: 4rem; text-align: center; background: #1f2937; color: white; font-family: Arial; min-height: 100vh;">
        <h1 style="color: #f59e0b; font-size: 3rem;">404 - Page non trouvée</h1>
        <p style="font-size: 1.2rem; margin: 2rem 0;">La page demandée n'existe pas.</p>
        <a href="/" style="background: #4f46e5; color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none;">
            ← Retour à l'accueil A LAIZ PROD
        </a>
    </div>
    """, 404

@app.errorhandler(500)
def internal_server_error(error):
    """Page 500 personnalisée"""
    return jsonify({
        'error': 'Erreur interne du serveur A LAIZ PROD',
        'contact': '+237 694723492',
        'email': 'contact@alaizopays.art'
    }), 500

# ============================================================================
# LANCEMENT DE L'APPLICATION
# ============================================================================

if __name__ == "__main__":
    # Configuration selon l'environnement
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 A LAIZ PROD - Démarrage de l'application")
    print("🎵 Les Nanfang - Yaoundé, Cameroun")
    print(f"🌐 Mode debug: {debug_mode}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
