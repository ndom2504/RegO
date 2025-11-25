# Guide de configuration Azure AD pour RegO

Ce guide détaille étape par étape comment configurer votre application Azure AD pour utiliser RegO.

## Étape 1: Accéder au portail Azure

1. Rendez-vous sur https://portal.azure.com
2. Connectez-vous avec votre compte Microsoft 365 professionnel
3. Dans la barre de recherche, tapez "Azure Active Directory" et sélectionnez le service

## Étape 2: Créer une nouvelle application

1. Dans le menu de gauche, cliquez sur **"App registrations"** (Inscriptions d'applications)
2. Cliquez sur **"+ New registration"** (Nouvelle inscription)
3. Remplissez le formulaire:
   - **Name** (Nom): `RegO` ou un nom de votre choix
   - **Supported account types** (Types de comptes pris en charge):
     - Sélectionnez "Accounts in this organizational directory only" 
     - (Comptes dans cet annuaire organisationnel uniquement)
   - **Redirect URI**: Laissez vide pour l'instant
4. Cliquez sur **"Register"** (Inscrire)

## Étape 3: Noter les informations importantes

Après la création, vous êtes redirigé vers la page "Overview" de votre application.

**⚠️ Copiez et sauvegardez ces informations:**

- **Application (client) ID**: Un GUID comme `12345678-1234-1234-1234-123456789abc`
- **Directory (tenant) ID**: Un autre GUID

## Étape 4: Créer un secret client

1. Dans le menu de gauche, cliquez sur **"Certificates & secrets"** (Certificats et secrets)
2. Sous l'onglet **"Client secrets"** (Secrets client), cliquez sur **"+ New client secret"**
3. Remplissez:
   - **Description**: `RegO Secret` ou une description claire
   - **Expires**: Choisissez une durée (recommandé: 24 mois)
4. Cliquez sur **"Add"** (Ajouter)
5. **⚠️ IMPORTANT:** Copiez immédiatement la **Value** (Valeur) du secret
   - Cette valeur ne sera plus affichée après avoir quitté cette page
   - Si vous la perdez, vous devrez créer un nouveau secret

## Étape 5: Configurer les permissions API

1. Dans le menu de gauche, cliquez sur **"API permissions"** (Autorisations API)
2. Supprimez les permissions par défaut (User.Read) si présente
3. Cliquez sur **"+ Add a permission"** (Ajouter une autorisation)
4. Sélectionnez **"Microsoft Graph"**
5. Choisissez **"Application permissions"** (Autorisations d'application)
6. Recherchez et ajoutez ces permissions:
   - **Mail.Read**: Permet de lire les emails
     - Tapez "Mail" dans la recherche
     - Cochez `Mail.Read` sous "Application permissions"
   - **User.Read.All**: Permet de lire les informations utilisateur
     - Tapez "User" dans la recherche
     - Cochez `User.Read.All` sous "Application permissions"
7. Cliquez sur **"Add permissions"** (Ajouter les autorisations)

## Étape 6: Accorder le consentement administrateur

**⚠️ Cette étape nécessite des privilèges d'administrateur**

1. Sur la page "API permissions", cliquez sur **"Grant admin consent for [Votre organisation]"**
2. Confirmez en cliquant sur **"Yes"**
3. Les permissions doivent maintenant afficher une coche verte avec "Granted for [Votre organisation]"

## Étape 7: Configurer le fichier .env

1. Dans le dossier RegO, créez un fichier `.env` (copiez `.env.example`)
2. Remplissez avec vos informations:

```env
CLIENT_ID=0bf5e2d3-8bd8-4018-bb93-574036e9da92
CLIENT_SECRET=votre_secret_client_value
TENANT_ID=79f19744-dc18-4e15-b6b9-a65e89211776
```

**⚠️ Important:** Remplacez `votre_secret_client_value` par la valeur secrète que vous avez copiée lors de l'étape 4.

**Vos informations (déjà configurées):**
- **CLIENT_ID**: `0bf5e2d3-8bd8-4018-bb93-574036e9da92` ✅
- **TENANT_ID**: `79f19744-dc18-4e15-b6b9-a65e89211776` ✅
- **CLIENT_SECRET**: À ajouter depuis Azure Portal > Certificats et secrets

## Vérification de la configuration

Pour vérifier que tout est correctement configuré:

1. Assurez-vous que votre fichier `.env` contient les 3 valeurs requises
2. Vérifiez que les permissions ont le consentement administrateur accordé
3. Lancez RegO: `python main.py`
4. Essayez l'option 1 "S'authentifier avec Outlook"

Si l'authentification réussit, vous verrez: ✅ Authentification réussie!

## Erreurs courantes et solutions

### "Invalid client secret"
- Le secret client est incorrect ou a expiré
- Créez un nouveau secret dans Azure AD

### "Insufficient privileges"
- Les permissions n'ont pas été accordées
- Vérifiez que vous avez cliqué sur "Grant admin consent"

### "AADSTS700016: Application not found"
- Le CLIENT_ID est incorrect
- Vérifiez l'Application ID dans Azure AD

### "AADSTS90002: Tenant not found"
- Le TENANT_ID est incorrect
- Vérifiez le Directory ID dans Azure AD

## Ressources supplémentaires

- [Documentation Microsoft Graph](https://docs.microsoft.com/en-us/graph/)
- [Azure AD App Registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Microsoft Graph Permissions](https://docs.microsoft.com/en-us/graph/permissions-reference)

## Support

Si vous rencontrez des problèmes, vérifiez:
1. Que vous êtes bien administrateur de votre tenant Azure AD
2. Que votre organisation autorise la création d'applications
3. Que toutes les informations copiées sont exactes (sans espaces supplémentaires)
