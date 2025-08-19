from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'alaiz-prod-secret-key-2025'

# Routes principales
@app.route("/")
def home():
    return render_template("index.html", page="accueil")

@app.route("/services")
def services():
    return render_template("index.html", page="services")

@app.route("/label")
def label():
    return render_template("index.html", page="label")

@app.route("/artiste")
def artiste():
    return render_template("index.html", page="artiste")

@app.route("/boutique")
def boutique():
    return render_template("index.html", page="boutique")

@app.route("/contact")
def contact():
    return render_template("index.html", page="contact")

# API Routes
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
    """API pour le chat IA"""
    data = request.get_json()
    message = data.get('message', '').lower()
    
    # Réponses IA simulées
    responses = {
        'bonjour': 'Bonjour ! Comment puis-je vous aider avec A LAIZ PROD aujourd\'hui ?',
        'services': 'Nous proposons des prestations artistiques, formations musicales, production et édition. Quel domaine vous intéresse ?',
        'prix': 'Nos tarifs varient selon le projet. Utilisez notre calculateur IA pour obtenir un devis personnalisé !',
        'formation': 'Nos formations intègrent l\'IA et la réalité augmentée pour un apprentissage révolutionnaire.',
        'contact': 'Vous pouvez nous contacter par email, téléphone ou WhatsApp. Préférez-vous programmer un rendez-vous virtuel ?',
        'technologie': 'Nous utilisons l\'IA, la blockchain, la VR/AR et l\'audio spatial pour révolutionner l\'art musical.',
    }
    
    # Recherche de mots-clés
    for keyword, response in responses.items():
        if keyword in message:
            return jsonify({
                'response': response,
                'timestamp': datetime.now().isoformat()
            })
    
    return jsonify({
        'response': 'C\'est une question intéressante ! Pouvez-vous me donner plus de détails pour mieux vous aider ?',
        'timestamp': datetime.now().isoformat()
    })

@app.route("/api/smart-form", methods=["POST"])
def smart_form():
    """API pour l'analyse IA du formulaire"""
    data = request.get_json()
    description = data.get('description', '').lower()
    
    suggestions = []
    
    if 'mariage' in description:
        suggestions.extend([
            '💍 Pack Mariage Premium avec captation 4K',
            '🎵 Playlist personnalisée avec IA'
        ])
    
    if 'formation' in description:
        suggestions.extend([
            '🎓 Formation certifiante avec VR',
            '📱 Accès à l\'app mobile AR'
        ])
    
    if 'concert' in description:
        suggestions.extend([
            '🎤 Sonorisation 3D immersive',
            '💡 Éclairage intelligent synchronisé'
        ])
    
    if not suggestions:
        suggestions = [
            '🎯 Consultation personnalisée recommandée',
            '📞 Entretien vidéo avec nos experts'
        ]
    
    return jsonify({
        'suggestions': suggestions,
        'analysis': 'Analyse IA terminée',
        'confidence': 95
    })

@app.route("/api/contact", methods=["POST"])
def submit_contact():
    """API pour soumission du formulaire de contact"""
    data = request.get_json()
    
    # Ici vous pourriez sauvegarder en base de données
    contact_data = {
        'name': data.get('name'),
        'email': data.get('email'),
        'project': data.get('project'),
        'timestamp': datetime.now().isoformat(),
        'status': 'received'
    }
    
    return jsonify({
        'status': 'success',
        'message': 'Votre demande a été reçue ! Nous vous contacterons sous 24h.',
        'reference': f'ALAIZ-{datetime.now().strftime("%Y%m%d%H%M%S")}'
    })

@app.route("/api/performance")
def api_performance():
    """API pour les métriques de performance"""
    import random
    
    return jsonify({
        'fps': random.randint(55, 60),
        'latency': random.randint(8, 15),
        'memory': random.randint(45, 65),
        'cpu': random.randint(20, 40)
    })

@app.errorhandler(404)
def not_found(error):
    return render_template("index.html", page="accueil"), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erreur interne du serveur'}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)