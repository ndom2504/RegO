# RegO - Registre Outlook 📧

Application Python pour capturer vos courriels Outlook professionnels et les stocker sous forme de registre exportable en PDF.

## 🌟 Fonctionnalités

- **Connexion sécurisée** à votre compte Outlook via Microsoft Graph API
- **Récupération des emails** avec tous les détails (expéditeur, destinataires, date, sujet, etc.)
- **Stockage en registre** au format JSON
- **Export PDF élégant** avec mise en forme professionnelle
- **Interface CLI intuitive** avec menus interactifs et affichage coloré
- **Statistiques complètes** sur vos emails

## 📋 Prérequis

- Python 3.8 ou supérieur
- Un compte Microsoft 365 / Outlook professionnel
- Une application Azure AD (voir section Configuration)

## 🚀 Installation

1. **Cloner ou télécharger le projet**
   ```bash
   cd RegO
   ```

2. **Créer un environnement virtuel**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur macOS/Linux
   # ou
   venv\Scripts\activate  # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

### 1. Créer une application Azure AD

1. Allez sur le [Azure Portal](https://portal.azure.com)
2. Naviguez vers **Azure Active Directory** > **App registrations** > **New registration**
3. Donnez un nom à votre application (ex: "RegO")
4. Pour **Supported account types**, choisissez "Accounts in this organizational directory only"
5. Cliquez sur **Register**

### 2. Configurer les permissions

1. Dans votre application, allez dans **API permissions**
2. Cliquez sur **Add a permission** > **Microsoft Graph** > **Application permissions**
3. Ajoutez les permissions suivantes:
   - `Mail.Read` (pour lire les emails)
   - `User.Read.All` (pour obtenir les infos utilisateur)
4. Cliquez sur **Grant admin consent** pour approuver les permissions

### 3. Créer un secret client

1. Allez dans **Certificates & secrets**
2. Cliquez sur **New client secret**
3. Donnez une description et choisissez une durée de validité
4. **Copiez la valeur du secret** (vous ne pourrez plus la voir après)

### 4. Configurer le fichier .env

1. Copiez le fichier `.env.example` en `.env`:
   ```bash
   cp .env.example .env
   ```

2. Remplissez les informations:
   ```env
   CLIENT_ID=votre_application_id
   CLIENT_SECRET=votre_secret_client
   TENANT_ID=votre_tenant_id
   ```

   Vous trouverez ces informations dans votre application Azure:
   - **CLIENT_ID**: "Application (client) ID" sur la page Overview
   - **TENANT_ID**: "Directory (tenant) ID" sur la page Overview
   - **CLIENT_SECRET**: Le secret que vous avez créé

## 💻 Utilisation

### Lancer l'application

```bash
python main.py
```

### Menu principal

L'application propose un menu interactif avec les options suivantes:

1. **🔐 S'authentifier avec Outlook** - Connectez-vous avec vos identifiants Azure
2. **📥 Récupérer les emails** - Téléchargez vos emails depuis Outlook
3. **📊 Voir les statistiques** - Affichez des stats sur vos emails
4. **📋 Voir la liste des emails** - Consultez la liste de vos emails
5. **📄 Exporter en PDF** - Générez un PDF professionnel de votre registre
6. **🗑️ Effacer le registre** - Supprimez tous les emails du registre
7. **❌ Quitter** - Fermez l'application

### Workflow typique

1. Lancez l'application: `python main.py`
2. Choisissez l'option 1 pour vous authentifier
3. Choisissez l'option 2 pour récupérer vos emails (spécifiez le nombre souhaité)
4. Consultez vos emails avec les options 3 ou 4
5. Exportez en PDF avec l'option 5
6. Les PDF sont sauvegardés dans le dossier `exports/`

## 📁 Structure du projet

```
RegO/
├── config/
│   └── settings.py          # Configuration de l'application
├── src/
│   ├── auth.py             # Authentification Microsoft Graph
│   ├── email_fetcher.py    # Récupération des emails
│   ├── registry.py         # Gestion du registre
│   └── pdf_exporter.py     # Export PDF
├── data/
│   └── email_registry.json # Registre des emails (généré)
├── exports/
│   └── *.pdf               # Fichiers PDF exportés
├── main.py                 # Point d'entrée de l'application
├── requirements.txt        # Dépendances Python
├── .env                    # Configuration (à créer)
└── .env.example           # Exemple de configuration
```

## 📄 Format du PDF exporté

Le PDF généré contient:
- **En-tête** avec vos informations et la date de génération
- **Statistiques** sur vos emails (total, lus/non lus, avec pièces jointes, etc.)
- **Liste détaillée** de chaque email avec:
  - Numéro de séquence
  - Sujet
  - Expéditeur
  - Destinataires (À et CC)
  - Date de réception
  - Statut (lu/non lu, pièces jointes, importance)
  - Aperçu du contenu

## 🔒 Sécurité

- Le fichier `.env` contient des informations sensibles et ne doit **jamais** être partagé ou commité dans Git
- Utilisez des secrets avec une durée de validité limitée
- Les tokens d'accès sont stockés uniquement en mémoire pendant l'exécution

## 🐛 Dépannage

### Erreur d'authentification

- Vérifiez que vos identifiants dans `.env` sont corrects
- Assurez-vous que les permissions ont été accordées dans Azure AD
- Vérifiez que le secret client n'a pas expiré

### Erreur de permissions

- Vérifiez que vous avez accordé le consentement administrateur dans Azure AD
- Assurez-vous d'avoir les permissions `Mail.Read` et `User.Read.All`

### Aucun email récupéré

- Vérifiez que votre boîte de réception contient des emails
- Essayez d'augmenter la limite de récupération
- Vérifiez les filtres de date dans `.env`

## 🤝 Support

Pour toute question ou problème, consultez la documentation Microsoft Graph API:
- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/api/overview)
- [Azure AD App Registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

## 📝 Licence

Ce projet est fourni tel quel pour usage personnel et professionnel.

---

**Développé avec ❤️ pour une meilleure gestion de vos courriels professionnels**
