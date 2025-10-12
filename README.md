# Alaiz Prod - Website API

## Présentation du projet

Ce projet est l'API backend du site web d'Alaiz Prod. Il s'agit d'une application Node.js/Express qui fournit des endpoints pour gérer les playlists et les commentaires.

### Fonctionnalités principales
- Gestion de playlists musicales
- Système de commentaires
- Intégration avec l'API Gemini pour des fonctionnalités avancées

## Installation

### Prérequis
- Node.js (version 14 ou supérieure)
- npm ou yarn

### Étapes d'installation

1. Cloner le dépôt :
```bash
git clone https://github.com/LeJuif69/alaiz-prod-website.git
cd alaiz-prod-website
```

2. Installer les dépendances :
```bash
npm install
```

3. Configurer les variables d'environnement :
Créez un fichier `.env` à la racine du projet et ajoutez :
```
GEMINI_API_KEY=votre_clé_api_ici
PORT=3000
```

4. Lancer le serveur :
```bash
node server.js
```

Le serveur démarre par défaut sur le port 3000.

## Instructions de test

### Installation des dépendances de test

Les dépendances de test (Jest et Supertest) sont déjà incluses dans le `package.json` :
```bash
npm install --save-dev jest supertest
```

### Lancer les tests

Pour exécuter tous les tests :
```bash
npm test
```

### Structure des tests

Les tests sont organisés dans le dossier `tests/` :
- `tests/playlist.test.js` : Tests pour l'endpoint de playlist
- `tests/comments.test.js` : Tests pour l'endpoint de commentaires

### Configuration Jest

La configuration Jest est définie dans `package.json` :
```json
{
  "jest": {
    "testEnvironment": "node"
  }
}
```

### Note importante

Les tests peuvent fonctionner sans la variable `GEMINI_API_KEY`. L'application utilise un système de fallback qui retourne des données de démonstration lorsque la clé API n'est pas configurée.

## Structure du projet

```
alaiz-prod-website/
├── server.js           # Point d'entrée de l'application
├── playlist.js         # Logique de gestion des playlists
├── comments.js         # Logique de gestion des commentaires
├── tests/
│   ├── playlist.test.js
│   └── comments.test.js
├── package.json
└── README.md
```

## Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

Ce projet est sous licence MIT.
