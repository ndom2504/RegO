# 🚀 Guide d'utilisation RegO - OAuth2 Microsoft

## ✨ Connexion automatique avec Microsoft (NOUVEAU!)

### Pour les utilisateurs:

#### **Option 1: Connexion avec Microsoft (Recommandé - SIMPLE)**

1. **Allez sur la page de connexion** : http://localhost:5000/login
2. **Cliquez sur "Se connecter avec Microsoft"** (bouton noir avec logo Microsoft)
3. **Authentifiez-vous** avec votre compte Microsoft/Outlook
4. **Autorisez l'application** RegO à accéder à vos emails
5. **C'EST TOUT!** 🎉

**Avantages:**
- ✅ Aucune configuration manuelle nécessaire
- ✅ Pas besoin de créer d'application Azure AD
- ✅ Sécurisé (OAuth2 standard)
- ✅ Compte créé automatiquement
- ✅ Emails synchronisés automatiquement

---

#### **Option 2: Connexion classique (Avancé)**

Si vous préférez créer un compte manuel:

1. **Créer un compte** : http://localhost:5000/register
   - Nom d'utilisateur
   - Email
   - Mot de passe

2. **Configurer Outlook manuellement** dans Configuration:
   - Client ID (Azure AD)
   - Client Secret
   - Tenant ID
   - Email Outlook

---

## 🔧 Configuration pour l'administrateur (Vous)

### Prérequis Azure AD

Votre application Azure AD doit avoir ces **permissions déléguées** (pour OAuth):

```
✅ openid
✅ profile
✅ email
✅ User.Read
✅ Mail.Read
✅ Mail.ReadBasic
```

### Configuration dans le Portail Azure

1. **Accédez à votre application Azure AD**
   - portal.azure.com → Azure Active Directory → App registrations

2. **Redirect URIs** (obligatoire!)
   Ajoutez ces URLs dans "Authentication" → "Redirect URIs":
   ```
   http://localhost:5000/auth/microsoft/callback
   ```
   
   Pour la production:
   ```
   https://votredomaine.com/auth/microsoft/callback
   ```

3. **Type de compte** (Important!)
   Sélectionnez:
   - ✅ **"Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts"**
   
   Cela permet à n'importe quel utilisateur Microsoft de se connecter!

4. **Permissions API**
   - Vérifiez que les permissions déléguées sont ajoutées
   - Cliquez sur "Grant admin consent" si vous êtes admin

---

## 🎯 Flux d'utilisation typique

### Nouvel utilisateur:

1. **Visite http://localhost:5000**
2. **Clic sur "Se connecter avec Microsoft"**
3. **Authentification Microsoft** (une seule fois)
4. **Autorisation** de l'app (une seule fois)
5. **Redirection automatique** vers le dashboard
6. **Emails disponibles** immédiatement!

### Utilisateur existant:

1. **Visite http://localhost:5000**
2. **Clic sur "Se connecter avec Microsoft"**
3. **Connexion instantanée** (pas de re-autorisation)
4. **Dashboard avec ses emails**

---

## 🔒 Sécurité

- Les tokens OAuth sont **stockés cryptés** dans la base de données
- Les tokens **expirent automatiquement** (3600 secondes)
- Les refresh tokens permettent **renouvellement automatique**
- **Aucun mot de passe stocké** pour les utilisateurs OAuth

---

## 💡 Avantages pour votre commercialisation

### Pour vos clients:
- ✅ **Onboarding ultra-simple**: 2 clics pour commencer
- ✅ **Pas de configuration technique** nécessaire
- ✅ **Connexion sécurisée** avec Microsoft
- ✅ **Expérience moderne** (comme Google OAuth)

### Pour vous:
- ✅ **Configuration centralisée**: Une seule Azure AD App
- ✅ **Multi-tenant**: Tous vos clients utilisent la même app
- ✅ **Moins de support**: Pas de confusion avec Client ID/Secret
- ✅ **Professionnel**: Standard OAuth2

---

## 📊 Modèle de tarification suggéré

### Plan Gratuit
- Connexion avec Microsoft ✅
- 100 emails synchronisés/mois
- Export PDF basique

### Plan Pro (29€/mois)
- Connexion avec Microsoft ✅
- Emails illimités
- Export PDF avancé
- Support prioritaire
- Catégories et tags

### Plan Entreprise (99€/mois)
- Tout du Plan Pro
- Configuration manuelle (Client ID/Secret) disponible
- Support dédié
- API access

---

## 🚀 Déploiement en production

### Variables d'environnement nécessaires:

```bash
# Azure AD OAuth (obligatoire)
MICROSOFT_CLIENT_ID=votre-client-id
MICROSOFT_CLIENT_SECRET=votre-client-secret
MICROSOFT_TENANT_ID=common  # Pour multi-tenant

# Flask
SECRET_KEY=votre-secret-key-super-securise

# Base de données
DATABASE_URL=postgresql://...  # Utilisez PostgreSQL en prod
```

### URLs de redirection à configurer:
```
Production: https://app.rego.com/auth/microsoft/callback
Staging: https://staging.rego.com/auth/microsoft/callback
Dev: http://localhost:5000/auth/microsoft/callback
```

---

## 📞 Support

Pour toute question sur la configuration OAuth:
- Documentation Microsoft: https://learn.microsoft.com/en-us/azure/active-directory/develop/
- Votre contact: info@misterdil.ca

---

**Félicitations! Votre application RegO est maintenant prête pour la commercialisation avec OAuth2! 🎉**
