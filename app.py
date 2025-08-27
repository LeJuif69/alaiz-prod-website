from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'alaiz-prod-secret-key-2025'

# Fonction pour charger les articles du blog
def load_articles():
    try:
        with open('data/articles.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Route principale - Accueil + À Propos
@app.route("/")
def index():
    """Page d'accueil avec présentation du duo"""
    return render_template("index.html", page="accueil")

# Services - Prestations + Boutique
@app.route("/services")
def services():
    """Page services avec prestations et produits"""
    return render_template("services.html", page="services")

# Formations - Cours et pédagogie
@app.route("/formations")
def formations():
    """Page formations avec cours et méthodes"""
    return render_template("formations.html", page="formations")

# Label - Production + Artistes
@app.route("/label")
def label():
    """Page label avec production et artistes"""
    return render_template("label.html", page="label")

# Blog - Liste des actualités
@app.route("/blog")
def blog():
    """Page blog avec liste des actualités"""
    articles = load_articles()
    # Trier par date décroissante
    articles.sort(key=lambda x: x.get('date', ''), reverse=True)
    return render_template("blog.html", page="blog", articles=articles)

# Article individuel
@app.route("/blog/<slug>")
def article(slug):
    """Page article individuel"""
    articles = load_articles()
    article = next((a for a in articles if a.get('slug') == slug), None)
    
    if not article:
        return redirect(url_for('blog'))
    
    return render_template("article.html", page="blog", article=article)

# Contact - Formulaire et coordonnées
@app.route("/contact")
def contact():
    """Page contact avec formulaire"""
    return render_template("contact.html", page="contact")

# API - Soumission formulaire contact
@app.route("/api/contact", methods=['POST'])
def api_contact():
    """API pour traitement formulaire contact"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error", 
                "message": "Aucune donnée reçue"
            }), 400
        
        # Validation des champs obligatoires
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "status": "error",
                    "message": f"Le champ {field} est obligatoire"
                }), 400
        
        # Log pour débogage (remplacer par envoi email en production)
        print(f"Nouveau contact reçu: {data}")
        
        # Génération URL WhatsApp pour transfert
        whatsapp_message = f"""Bonjour A LAIZ PROD,

Je suis {data.get('name')}.
Email: {data.get('email')}
Téléphone: {data.get('phone', 'Non renseigné')}

Type de prestation: {data.get('service', 'Non spécifié')}
Date souhaitée: {data.get('date', 'Non spécifiée')}
Budget: {data.get('budget', 'Non spécifié')}

Message:
{data.get('message')}"""
        
        return jsonify({
            "status": "success",
            "message": "Message envoyé avec succès!",
            "whatsapp_url": f"https://wa.me/237694723492?text={whatsapp_message}",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Erreur API contact: {e}")
        return jsonify({
            "status": "error",
            "message": "Erreur lors de l'envoi"
        }), 500

# API - Statut du service
@app.route("/api/status")
def api_status():
    """API de statut pour monitoring"""
    return jsonify({
        "status": "online",
        "service": "A LAIZ PROD Website",
        "version": "2.0-restructured",
        "timestamp": datetime.now().isoformat(),
        "routes_loaded": len([rule.rule for rule in app.url_map.iter_rules()])
    })

# Route de test pour vérifications
@app.route("/test")
def test():
    """Route de test pour vérifier le déploiement"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test A LAIZ PROD</title>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1 style="color: #4f46e5;">✅ Site A LAIZ PROD Fonctionnel</h1>
        <p>Nouvelle structure déployée avec succès</p>
        <p><strong>Routes disponibles:</strong></p>
        <ul style="list-style: none; padding: 0;">
            <li><a href="/">/</a> - Accueil</li>
            <li><a href="/services">/services</a> - Services</li>
            <li><a href="/formations">/formations</a> - Formations</li>
            <li><a href="/label">/label</a> - Label</li>
            <li><a href="/blog">/blog</a> - Actualités</li>
            <li><a href="/contact">/contact</a> - Contact</li>
        </ul>
        <p style="color: #6b7280; margin-top: 2rem;">
            Test effectué le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
        </p>
    </body>
    </html>
    """

# Gestion d'erreur 404
@app.errorhandler(404)
def page_not_found(e):
    """Page d'erreur 404 personnalisée"""
    return render_template("404.html"), 404

# Gestion d'erreur 500
@app.errorhandler(500)
def internal_error(e):
    """Page d'erreur 500 personnalisée"""
    return render_template("500.html"), 500

# Démarrage de l'application
if __name__ == "__main__":
    # Création du dossier data s'il n'existe pas
    os.makedirs('data', exist_ok=True)
    
    # Mode développement local
    app.run(
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 5000)), 
        debug=True
    )
else:
    # Mode production (Render)
    print(f"🚀 A LAIZ PROD Website v2.0 démarré")
    print(f"📅 {datetime.now()}")
    print(f"🔗 Routes: {len([rule.rule for rule in app.url_map.iter_rules()])}")
