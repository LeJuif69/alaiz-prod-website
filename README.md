# 🎵 A Laiz Prod - Site Web Premium

Site web professionnel pour A Laiz Prod, duo musical camerounais d'exception (Flavie & Hervé Nanfang).

## ✨ Fonctionnalités

- **Design Modern & Responsive** - Interface premium adaptée mobile/desktop
- **Sections Complètes** - Accueil, Services, À Propos, Formations, Contact
- **Formulaire de Contact** - Avec validation et envoi email automatique
- **Animations Fluides** - Micro-interactions et animations au scroll
- **SEO Optimisé** - Balises meta, données structurées
- **Performance Optimisée** - Chargement rapide, compression assets
- **Pages d'Erreur Personnalisées** - 404/500 avec design cohérent

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- Git

### 1. Cloner le Projet
```bash
git clone https://github.com/votre-username/alaiz-prod.git
cd alaiz-prod
```

### 2. Environnement Virtuel
```bash
# Créer l'environnement virtuel
python -m venv venv
# Activer (Linux/Mac)
source venv/bin/activate
# Activer (Windows)
venv\Scripts\activate
```

### 3. Installer les Dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration
```bash
# Copier le fichier d'environnement
cp .env.example .env
# Éditer .env avec vos vraies valeurs
nano .env
```

### 5. Lancer en Développement
```bash
python app.py
```

Le site sera accessible sur `http://localhost:5000`

## ⚙️ Configuration Détaillée

### Variables d'Environnement (.env)
```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Email Configuration (pour le formulaire de contact)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=votre-email@gmail.com
EMAIL_PASSWORD=votre-mot-de-passe-app
EMAIL_USE_TLS=True
EMAIL_RECIPIENT=contact@alaizprod.com

# Render Deployment
PORT=5000
```

### Structure du Projet
```
alaiz-prod-website/
├── app.py                 # Application Flask principale
├── render.yaml           # Configuration Render
├── requirements.txt      # Dépendances Python
├── runtime.txt          # Version Python
├── Procfile            # Configuration Heroku/Render
├── .env                # Variables d'environnement
├── static/             # Assets statiques (CSS, JS, images)
├── templates/          # Templates Jinja2
├── components/         # Composants réutilisables
├── data/              # Fichiers de données
├── assets/            # Images et médias
└── tests/             # Tests automatisés
```

## 🔧 Backend - Architecture & Documentation

### Workflow Render - Déploiement Automatique

#### 1. Push Backend (Flask/Python)
- **Trigger** : Push sur branche `main` ou `feature/restructure`
- **Action** : Render détecte les changements dans `app.py`, `requirements.txt`, `render.yaml`
- **Processus** :
  1. Installation automatique des dépendances (`pip install -r requirements.txt`)
  2. Reconstruction de l'API Flask avec Gunicorn
  3. Redémarrage automatique du service backend
  4. Tests de santé via endpoint `/health`
- **Temps** : ~2-3 minutes
- **URL Live** : Backend API accessible immédiatement

#### 2. Push Frontend (Templates/Static)
- **Trigger** : Modifications dans `/templates`, `/static`, `/components`
- **Action** : Render reconstruit le site statique automatiquement
- **Processus** :
  1. Compilation des templates Jinja2
  2. Minification CSS/JS automatique
  3. Optimisation des images
  4. Mise en cache CDN
- **Temps** : ~1-2 minutes
- **URL Live** : Site web mis à jour instantanément

### API Endpoints Documentation

#### 1. `/health` - Endpoint de Santé
**Méthode** : `GET`
**Description** : Vérification de l'état du backend
**Réponse** :
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "database": "connected",
  "email_service": "operational"
}
```
**Usage** : Surveillance automatique, monitoring Render

#### 2. `/contact` - Formulaire de Contact
**Méthode** : `POST`
**Description** : Traitement des messages de contact
**Paramètres** :
```json
{
  "name": "string (required)",
  "email": "string (required, valid email)",
  "subject": "string (required)",
  "message": "string (required, min 10 chars)",
  "phone": "string (optional)"
}
```
**Réponses** :
- **200** : Message envoyé avec succès
- **400** : Erreur de validation
- **500** : Erreur serveur/email

#### 3. `/playlist` - Gestion Playlists (Future)
**Méthode** : `GET`, `POST`
**Description** : Gestion des playlists musicales A Laiz Prod
**Fonctionnalités prévues** :
- Récupération des playlists Spotify/YouTube
- Création de playlists personnalisées
- Intégration avec les services de streaming

### Structure Communication Frontend ↔ Backend

#### 1. Architecture de Communication
```
Frontend (Templates Jinja2)
        ↓
   AJAX Requests
        ↓
Backend Flask API
        ↓
   Database/Services
        ↓
   JSON Response
        ↓
   Frontend Update
```

#### 2. Flux de Données - Formulaire Contact
```javascript
// Frontend - Envoi de formulaire
fetch('/contact', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  },
  body: JSON.stringify(formData)
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    showSuccessMessage(data.message);
  } else {
    showErrorMessage(data.error);
  }
});
```

#### 3. Backend - Traitement et Réponse
```python
@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        # Validation des données
        if not validate_contact_form(data):
            return jsonify({'error': 'Données invalides'}), 400
        
        # Envoi email
        send_email(data)
        
        return jsonify({
            'success': True,
            'message': 'Message envoyé avec succès'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Conseils de Surveillance et Maintenance

#### 1. Monitoring Automatique
```bash
# Vérification de santé toutes les 5 minutes
curl -f https://alaiz-prod-backend.onrender.com/health || alert_admin

# Logs en temps réel
render logs --app alaiz-prod-backend --tail

# Métriques de performance
render metrics --app alaiz-prod-backend
```

#### 2. Alertes Critiques à Surveiller
- **Santé API** : Réponse `/health` > 5 secondes
- **Taux d'erreur** : > 5% d'erreurs 5xx
- **Mémoire** : Utilisation > 80%
- **Email** : Échec d'envoi de formulaires
- **SSL** : Expiration certificat < 30 jours

#### 3. Maintenance Préventive Mensuelle
```bash
# Mise à jour des dépendances
pip install -r requirements.txt --upgrade
pip freeze > requirements.txt

# Nettoyage des logs
render logs --clear --app alaiz-prod-backend

# Test des endpoints
curl -X POST https://alaiz-prod-backend.onrender.com/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","subject":"Test","message":"Test message"}'

# Vérification de la base de données
python -c "from app import test_db_connection; test_db_connection()"
```

#### 4. Plan de Récupération d'Urgence
**En cas de panne critique :**
1. **Diagnostic rapide** : Vérifier `/health` et logs Render
2. **Rollback** : Retour à la version précédente stable
3. **Communication** : Notification clients via page de statut
4. **Correction** : Fix en mode maintenance
5. **Tests** : Validation complète avant remise en production

#### 5. Optimisations de Performance
```python
# Cache Redis pour les réponses fréquentes
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/health')
@cache.cached(timeout=60)
def health():
    return jsonify({'status': 'healthy'})

# Compression GZIP
from flask_compress import Compress
Compress(app)

# Rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/contact', methods=['POST'])
@limiter.limit("5 per minute")
def contact():
    # ... code existant
```

### Mises à Jour
```bash
# Mettre à jour les dépendances
pip install -r requirements.txt --upgrade
```

## ❓ Dépannage

### Problèmes Courants

**1. Formulaire de contact ne fonctionne pas**
- Vérifier la configuration EMAIL_* dans `.env`
- Tester avec un autre service SMTP (Mailgun, SendGrid)

**2. CSS/JS ne se charge pas**
- Vérifier les chemins dans les templates
- Vider le cache navigateur
- Vérifier les permissions des fichiers

**3. Erreur 500 au démarrage**
- Vérifier les variables d'environnement
- Voir les logs Flask : `python app.py`
- Vérifier les imports Python

**4. Site lent**
- Compresser les images
- Activer la mise en cache
- Utiliser un CDN pour les assets

## 🤝 Support

### Contact Technique
- **Email** : contact@alaizprod.com
- **Téléphone** : +237 XXX XXX XXX

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

## 📄 Licence

© 2024 A Laiz Prod. Tous droits réservés.

---

**Développé avec ❤️ pour l'excellence musicale camerounaise**

🎵 *"Chaque note compte, chaque détail importe"* - A Laiz Prod
