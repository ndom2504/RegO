# 🎨 RegO Professional - Dashboard Multi-Utilisateurs avec OAuth2

## 🚀 NOUVELLE VERSION PROFESSIONNELLE

RegO dispose maintenant d'une version **professionnelle et commercialisable** avec:

### ✨ Fonctionnalités Principales

#### 🔐 Authentification Multi-Utilisateurs (NOUVEAU! OAuth2)
- **Connexion avec Microsoft** en 1 clic (OAuth2)
- Système de connexion/inscription classique
- Gestion des sessions sécurisées
- Profils utilisateurs personnalisés
- Chaque utilisateur a son propre registre
- **Aucune configuration technique nécessaire pour l'utilisateur!**

#### 📊 Dashboard Moderne
- Design professionnel et élégant
- Statistiques en temps réel
- Tableaux interactifs avec filtres
- Interface responsive

#### 📧 Registre des Communications
- Base de données SQL (SQLite)
- Import depuis Outlook automatique (OAuth2)
- Import manuel avec configuration Azure AD
- Catégorisation et tags
- Notes personnalisées
- Export PDF

#### 🎨 Design Premium
- Logo RegO intégré
- Couleurs de marque (bleu #1a5490)
- Animations fluides
- Interface intuitive

## 🏃 Démarrage Rapide

### 1. Installer les nouvelles dépendances

```bash
pip install flask-login flask-sqlalchemy werkzeug authlib
```

### 2. Configurer Azure AD (IMPORTANT!)

**Consultez `CONFIGURATION_AZURE.md` pour les instructions détaillées**

Résumé rapide:
1. Portail Azure → App registrations
2. Ajoutez Redirect URI: `http://localhost:5000/auth/microsoft/callback`
3. Permissions déléguées: `openid`, `profile`, `email`, `User.Read`, `Mail.Read`

### 3. Lancer l'application professionnelle

```bash
python app_pro.py
```

### 4. Accéder au dashboard

Ouvrez votre navigateur sur: **http://localhost:5000**

### 4. Se connecter

**Compte admin par défaut:**
- Nom d'utilisateur: `admin`
- Mot de passe: `admin123`

⚠️ **Important:** Changez ce mot de passe après la première connexion!

## 📁 Structure de la Base de Données

### Table `users`
- Informations utilisateur
- Configuration Outlook personnalisée
- Authentification sécurisée

### Table `communications`
- Emails/communications par utilisateur
- Métadonnées complètes
- Catégories et tags
- Notes personnalisées

## 🔧 Configuration par Utilisateur

Chaque utilisateur peut configurer sa propre connexion Outlook:

1. **Se connecter au dashboard**
2. **Aller dans "Profil"**
3. **Renseigner:**
   - Email Outlook
   - CLIENT_ID Azure
   - CLIENT_SECRET Azure
   - TENANT_ID Azure

## 🎯 Workflow d'Utilisation

### Pour un nouvel utilisateur:

1. **Inscription**
   - Créer un compte sur `/register`
   - Renseigner: username, email, mot de passe

2. **Configuration Outlook**
   - Aller dans le profil
   - Ajouter les identifiants Azure AD

3. **Authentification Outlook**
   - Cliquer sur "Authentifier Outlook"
   - Obtenir l'accès à la boîte mail

4. **Import des Communications**
   - Cliquer sur "Récupérer les emails"
   - Choisir le nombre
   - Les emails sont enregistrés dans le registre

5. **Gestion du Registre**
   - Voir toutes les communications
   - Filtrer, rechercher
   - Ajouter des catégories/tags
   - Ajouter des notes
   - Exporter en PDF

## 🆚 Différences avec la version simple

| Fonctionnalité | Version Simple | Version Pro |
|----------------|----------------|-------------|
| Multi-utilisateurs | ❌ | ✅ |
| Base de données | JSON | SQL |
| Authentification | ❌ | ✅ |
| Profils | ❌ | ✅ |
| Config par utilisateur | ❌ | ✅ |
| Catégorisation | ❌ | ✅ |
| Tags | ❌ | ✅ |
| Notes | ❌ | ✅ |
| Recherche avancée | ❌ | ✅ |
| Filtres | ❌ | ✅ |
| Pagination | ❌ | ✅ |
| Design | Simple | Premium |

## 🎨 Personnalisation

### Logo
Remplacez le logo dans:
```
static/img/logo.png
```

### Couleurs
Modifiez les couleurs dans les fichiers CSS:
- Couleur principale: `#1a5490`
- Couleur secondaire: `#0d2d52`

### Nom de l'entreprise
Modifiez dans les templates HTML

## 🔒 Sécurité

### En Production:

1. **Changer la SECRET_KEY**
   ```python
   app.config['SECRET_KEY'] = 'votre-cle-secrete-complexe'
   ```

2. **Désactiver le mode debug**
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

3. **Utiliser HTTPS**
   - Certificat SSL requis

4. **Base de données**
   - Passer de SQLite à PostgreSQL/MySQL pour la production

5. **Mots de passe**
   - Politique de mots de passe forts
   - Récupération de mot de passe

## 📊 API Endpoints

### Authentification
- `GET/POST /login` - Connexion
- `GET/POST /register` - Inscription
- `GET /logout` - Déconnexion

### Dashboard
- `GET /` - Dashboard principal
- `GET /communications` - Registre
- `GET /profile` - Profil

### API
- `GET /api/user/info` - Infos utilisateur
- `POST /api/user/update-outlook` - Config Outlook
- `POST /api/authenticate-outlook` - Auth Outlook
- `POST /api/fetch-communications` - Import emails
- `GET /api/communications` - Liste (avec filtres)
- `GET/PUT/DELETE /api/communications/<id>` - Détails
- `GET /api/stats` - Statistiques
- `POST /api/export-pdf` - Générer PDF
- `GET /api/download-pdf/<filename>` - Télécharger PDF

## 🚀 Déploiement

### Local
```bash
python app_pro.py
```

### Serveur avec Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_pro:app
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app_pro:app"]
```

## 💼 Commercialisation

### Prix suggéré
- **Plan Starter**: 29€/mois - 1 utilisateur
- **Plan Business**: 99€/mois - 10 utilisateurs
- **Plan Enterprise**: 299€/mois - Illimité

### Fonctionnalités Premium (à ajouter)
- [ ] Rapports avancés
- [ ] Export Excel
- [ ] Intégration API
- [ ] Notifications email
- [ ] Dashboard analytics
- [ ] Multi-tenant (SaaS)

## 📝 TODO pour la commercialisation

- [ ] Ajouter la récupération de mot de passe
- [ ] Implémenter les rôles (admin, user, viewer)
- [ ] Ajouter des templates d'emails
- [ ] Système de facturation
- [ ] Page de tarification
- [ ] Documentation API complète
- [ ] Tests automatisés
- [ ] Monitoring et logs
- [ ] Backup automatique
- [ ] Multi-langue (i18n)

## 🆘 Support

Pour toute question:
- Documentation: `/docs` (à créer)
- Email: support@rego.com (à configurer)

---

**RegO Professional - Votre registre de communications professionnelles** 🚀
