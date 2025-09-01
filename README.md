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

### Variables d'Environnement Critiques

Modifiez le fichier `.env` avec vos vraies informations :

```bash
# Coordonnées réelles
FLAVIE_PHONE=+237XXXXXXXXX
HERVE_PHONE=+237XXXXXXXXX
CONTACT_EMAIL=contact@alaizprod.com

# Email (pour formulaire de contact)
EMAIL_USER=votre_email@gmail.com
EMAIL_PASS=votre_mot_de_passe_app

# Réseaux sociaux
FACEBOOK_URL=https://facebook.com/alaizprod
INSTAGRAM_URL=https://instagram.com/alaizprod
YOUTUBE_URL=https://youtube.com/alaizprod
WHATSAPP_URL=https://wa.me/237XXXXXXXXX
```

### Configuration Gmail

Pour le formulaire de contact, configurez un mot de passe d'application Gmail :

1. **Activer la 2FA** sur votre compte Gmail
2. **Générer un mot de passe d'application** :
   - Aller dans Paramètres Google > Sécurité
   - Mots de passe des applications
   - Générer pour "Mail"
3. **Utiliser ce mot de passe** dans `EMAIL_PASS`

## 📁 Structure du Projet

```
alaiz-prod/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── .env                  # Variables d'environnement (à créer)
├── .env.example          # Exemple de configuration
├── .gitignore           # Fichiers à ignorer par Git
├── README.md            # Documentation
│
├── templates/           # Templates HTML
│   ├── base.html       # Template de base
│   ├── index.html      # Page d'accueil
│   ├── services.html   # Page services
│   ├── about.html      # Page à propos
│   ├── formations.html # Page formations
│   ├── contact.html    # Page contact
│   ├── 404.html        # Page erreur 404
│   └── 500.html        # Page erreur 500
│
└── static/             # Fichiers statiques
    ├── css/
    │   └── style.css   # CSS principal
    ├── js/
    │   └── main.js     # JavaScript principal
    └── images/         # Images (à ajouter)
        ├── hero-bg.jpg
        ├── team/
        └── favicon.ico
```

## 🎨 Personnalisation

### Remplacer le Contenu Placeholder

**⚠️ IMPORTANT - À faire avant mise en production :**

1. **Coordonnées** dans `app.py` et templates :
   ```python
   # Remplacer dans app.py, ligne ~50
   'phone': '+237 XXX XXX XXX'  # → Vrais numéros
   ```

2. **Images** :
   - Ajouter vraies photos dans `static/images/`
   - Photo du duo pour la section "À Propos"
   - Photo d'Hervé en situation d'enseignement
   - Image de fond pour le hero

3. **Réseaux Sociaux** :
   - Remplacer tous les liens `#` par les vraies URLs
   - Vérifier tous les templates

### Couleurs et Branding

Les couleurs sont définies dans `static/css/style.css` :

```css
:root {
    --primary-color: #2D3748;    /* Indigo foncé */
    --secondary-color: #D69E2E;  /* Or élégant */
    --accent-color: #FEFEFE;     /* Blanc crème */
}
```

## 🚢 Déploiement Production

### Option 1 : Déploiement Simple

```bash
# Installer gunicorn
pip install gunicorn

# Lancer en production
gunicorn --bind 0.0.0.0:5000 app:app
```

### Option 2 : Déploiement avec Nginx

1. **Configuration Nginx** (`/etc/nginx/sites-available/alaizprod`):
```nginx
server {
    listen 80;
    server_name alaizopays.art www.alaizopays.art;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/your/alaiz-prod/static;
        expires 30d;
    }
}
```

2. **Activer le site** :
```bash
sudo ln -s /etc/nginx/sites-available/alaizprod /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

3. **SSL avec Let's Encrypt** :
```bash
sudo certbot --nginx -d alaizopays.art -d www.alaizopays.art
```

### Option 3 : Déploiement sur Plateforme Cloud

**Heroku** :
```bash
# Procfile
echo "web: gunicorn app:app" > Procfile

# Déploiement
heroku create alaiz-prod
git push heroku main
```

**Vercel/Netlify** : Compatible avec adaptations mineures

## 🔍 SEO et Performance

### Optimisations Incluses
- ✅ Balises meta dynamiques
- ✅ Données structurées (Schema.org)
- ✅ Sitemap automatique
- ✅ Compression CSS/JS
- ✅ Lazy loading images
- ✅ Cache headers
- ✅ Mobile-first responsive

### Tests Recommandés
- **PageSpeed Insights** : Objectif 90+/100
- **Mobile-Friendly Test** : Google
- **Lighthouse Audit** : Performance, SEO, Accessibility

## 📊 Analytics

### Google Analytics (Optionnel)
Décommenter dans `templates/base.html` :
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
```

### Facebook Pixel (Optionnel)
Ajouter votre pixel ID dans les variables d'environnement.

## 🛠️ Maintenance

### Logs
```bash
# Voir les logs en temps réel
tail -f logs/alaiz-prod.log
```

### Backup
```bash
# Backup automatique (ajouter au cron)
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz app.py templates/ static/ .env
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
