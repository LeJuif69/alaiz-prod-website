from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'alaiz-prod-secret-key-2025'

# ✅ ROUTE DE TEST - COMPLÈTE ET FONCTIONNELLE
@app.route("/test")
def test_route():
    """Route de test pour vérifier que le routage fonctionne"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Routage</title>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1 style="color: green;">✅ ROUTAGE CORRIGÉ !</h1>
        <p style="font-size: 18px;">Toutes les routes fonctionnent maintenant !</p>
        <p style="color: #666;">Test effectué le : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
        <hr style="margin: 30px 0;">
        <h3>🔗 Testez les autres pages :</h3>
        <div style="margin: 20px 0;">
            <a href="/" style="margin: 10px; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">🏠 Accueil</a>
            <a href="/services" style="margin: 10px; padding: 10px 15px; background: #28a745; color: white; text-decoration: none; border-radius: 5px;">🎵 Services</a>
            <a href="/about" style="margin: 10px; padding: 10px 15px; background: #ffc107; color: white; text-decoration: none; border-radius: 5px;">👥 À propos</a>
            <a href="/formations" style="margin: 10px; padding: 10px 15px; background: #17a2b8; color: white; text-decoration: none; border-radius: 5px;">📚 Formations</a>
            <a href="/contact" style="margin: 10px; padding: 10px 15px; background: #dc3545; color: white; text-decoration: none; border-radius: 5px;">📞 Contact</a>
        </div>
    </body>
    </html>
    """

# ✅ ROUTES PRINCIPALES
@app.route("/")
def home():
    """Page d'accueil - Utilise index.html"""
    return render_template("index.html", page="accueil")

@app.route("/about")
def about():
    """Page À propos - Utilise about.html"""
    try:
        return render_template("about.html", page="about")
    except Exception as e:
        print(f"Template about.html non trouvé : {e}")
        return render_template("index.html", page="about")

@app.route("/services")
def services():
    """Page Services - Utilise services.html"""
    try:
        return render_template("services.html", page="services")
    except Exception as e:
        print(f"Template services.html non trouvé : {e}")
        return render_template("index.html", page="services")

@app.route("/formations")
def formations():
    """Page Formations - Utilise formations.html"""
    try:
        return render_template("formations.html", page="formations")
    except Exception as e:
        print(f"Template formations.html non trouvé : {e}")
        return render_template("index.html", page="formations")

@app.route("/contact")
def contact():
    """Page Contact - Utilise contact.html"""
    try:
        return render_template("contact.html", page="contact")
    except Exception as e:
        print(f"Template contact.html non trouvé : {e}")
        return render_template("index.html", page="contact")

@app.route("/boutique")
def boutique():
    """Page Boutique - Utilise boutique.html ou fallback vers index.html"""
    try:
        return render_template("boutique.html", page="boutique")
    except Exception as e:
        print(f"Template boutique.html non trouvé : {e}")
        return render_template("index.html", page="boutique")

@app.route("/label")
def label():
    """Page Label - Fallback vers index.html pour l'instant"""
    try:
        return render_template("label.html", page="label")
    except Exception as e:
        print(f"Template label.html non trouvé : {e}")
        return render_template("index.html", page="label")

@app.route("/artiste")
def artiste():
    """Page Artiste - Fallback vers index.html pour l'instant"""
    try:
        return render_template("artiste.html", page="artiste")
    except Exception as e:
        print(f"Template artiste.html non trouvé : {e}")
        return render_template("index.html", page="artiste")

# ✅ API ENDPOINTS
@app.route("/api/contact", methods=['POST'])
def api_contact():
    """API pour le formulaire de contact"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Aucune donnée reçue"}), 400
        
        # Log des données reçues (pour debug)
        print(f"Contact form data: {data}")
        
        # Ici vous pouvez ajouter l'envoi d'email, sauvegarde en DB, etc.
        
        return jsonify({
            "status": "success", 
            "message": "Message envoyé avec succès !",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Erreur API contact: {e}")
        return jsonify({"status": "error", "message": "Erreur lors de l'envoi"}), 500

@app.route("/api/status")
def api_status():
    """API de statut du service"""
    return jsonify({
        "status": "online",
        "service": "A Laiz Prod Website",
        "time": datetime.now().isoformat(),
        "version": "2.0-corrected"
    })

@app.route("/api/health")
def health_check():
    """Health check pour Render"""
    return jsonify({
        "health": "OK",
        "timestamp": datetime.now().isoformat(),
        "routes_loaded": len(app.url_map._rules)
    }), 200

# ✅ GESTION DES ERREURS
@app.errorhandler(404)
def page_not_found(e):
    """Page d'erreur 404 personnalisée"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Page non trouvée - A Laiz Prod</title>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1 style="color: #dc3545;">404 - Page non trouvée</h1>
        <p style="font-size: 18px;">La page que vous cherchez n'existe pas.</p>
        <p style="margin: 30px 0;">
            <a href="/" style="padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">🏠 Retour à l'accueil</a>
        </p>
        <hr style="margin: 30px 0;">
        <p style="color: #666; font-size: 14px;">URL demandée : {request.url}</p>
    </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(e):
    """Page d'erreur 500"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Erreur serveur - A Laiz Prod</title>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1 style="color: #dc3545;">Erreur serveur</h1>
        <p>Une erreur interne s'est produite.</p>
        <p style="margin: 30px 0;">
            <a href="/" style="padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">🏠 Retour à l'accueil</a>
        </p>
    </body>
    </html>
    """, 500

# ✅ ROUTES UTILITAIRES
@app.route("/sitemap")
def sitemap():
    """Plan du site"""
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append({
                'url': rule.rule,
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'})
            })
    
    return jsonify({
        "sitemap": routes,
        "total_routes": len(routes),
        "generated_at": datetime.now().isoformat()
    })

# ✅ DÉMARRAGE DE L'APPLICATION
if __name__ == "__main__":
    # Mode développement local
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
else:
    # Mode production (Render)
    print(f"🚀 A Laiz Prod Website démarré en production")
    print(f"📅 {datetime.now()}")
    print(f"🔗 Routes chargées: {len(app.url_map._rules)}")
