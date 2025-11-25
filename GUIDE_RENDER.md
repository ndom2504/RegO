# 🚀 Guide Déploiement Render.com

## 📋 Étapes Complètes

### 1️⃣ Créer compte Render (2 minutes)

1. **Allez sur**: https://render.com
2. **Sign Up** avec:
   - GitHub (recommandé pour déploiement facile)
   - OU Email/Google
3. Vérifiez votre email

---

### 2️⃣ Préparer le code (optionnel - déjà fait!)

✅ `requirements.txt` - Mis à jour avec gunicorn et authlib
✅ `app_pro.py` - Application Flask prête
✅ Tous les fichiers nécessaires

---

### 3️⃣ Déployer sur Render

#### Option A: Via GitHub (RECOMMANDÉ)

1. **Créez un repo GitHub** (si pas déjà fait):
   ```bash
   cd /Users/morelsttevensndong/RegO
   git init
   git add .
   git commit -m "Initial commit - RegO app"
   # Créez un repo sur GitHub puis:
   git remote add origin https://github.com/[VOTRE-USERNAME]/RegO.git
   git push -u origin main
   ```

2. **Sur Render.com**:
   - **New** → **Web Service**
   - **Connect GitHub repository**
   - Autorisez Render à accéder à votre repo
   - Sélectionnez le repo **RegO**

#### Option B: Upload Manuel (Plus simple si pas de GitHub)

1. **Sur Render.com**:
   - **New** → **Web Service**
   - **Public Git repository**
   - OU utilisez l'upload direct (si disponible)

---

### 4️⃣ Configuration du Service

Une fois le repo connecté, configurez:

**Basic Settings:**
- **Name**: `rego-ocean-factory`
- **Region**: `Oregon (US West)` ou `Ohio (US East)`
- **Branch**: `main`
- **Root Directory**: (laissez vide)

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  gunicorn app_pro:app
  ```

**Instance Type:**
- **Free** (pour tester)
- OU **Starter** (7$/mois - plus stable)

---

### 5️⃣ Variables d'Environnement

Dans **Environment**, ajoutez:

```bash
# Générez d'abord une clé secrète:
# Exécutez dans votre terminal: openssl rand -hex 32
FLASK_SECRET_KEY=VOTRE_CLE_GENEREE_ICI

MICROSOFT_CLIENT_ID=0bf5e2d3-8bd8-4018-bb93-574036e9da92

# Trouvez dans Azure Portal → App registrations → Certificates & secrets
MICROSOFT_CLIENT_SECRET=VOTRE_SECRET_AZURE_ICI

MICROSOFT_TENANT_ID=common
```

**Pour générer FLASK_SECRET_KEY:**
```bash
openssl rand -hex 32
```

---

### 6️⃣ Déployer!

1. Cliquez **Create Web Service**
2. Render va:
   - ✅ Cloner votre code
   - ✅ Installer les dépendances
   - ✅ Démarrer l'application
   - ✅ Vous donner une URL: `https://rego-ocean-factory.onrender.com`

**Attendez 3-5 minutes** pour le premier déploiement.

---

### 7️⃣ Tester l'Application

Une fois déployé:

1. Ouvrez: `https://rego-ocean-factory.onrender.com`
2. Vous devriez voir la page de login RegO
3. **NE PAS tester Microsoft login encore** (domaine pas encore configuré)

---

### 8️⃣ Ajouter Domaine Personnalisé

Dans Render Dashboard:

1. **Settings** → **Custom Domain**
2. Cliquez **Add Custom Domain**
3. Entrez: `ocean-factory.ca`
4. Render vous donnera des instructions DNS

**Vous verrez quelque chose comme:**
```
CNAME record needed:
ocean-factory.ca → rego-ocean-factory.onrender.com
```

---

### 9️⃣ Configurer DNS GoDaddy

Dans votre panneau GoDaddy:

1. **DNS** → **Manage Zones** → `ocean-factory.ca`

2. **Supprimez** les anciens records (CNAME _domainconnect, etc.)

3. **Ajoutez ces nouveaux records:**

**Pour le domaine principal:**
```
Type: CNAME
Name: @
Value: rego-ocean-factory.onrender.com
TTL: 600 (10 min)
```

**Pour www:**
```
Type: CNAME
Name: www
Value: rego-ocean-factory.onrender.com
TTL: 600
```

4. **Sauvegardez**

⚠️ **Note**: Si GoDaddy ne permet pas CNAME pour `@`, utilisez:
```
Type: A
Name: @
Value: [IP fournie par Render]
```

---

### 🔟 Vérifier la Propagation DNS

Attendez 5-30 minutes, puis testez:

```bash
# Vérifiez DNS
nslookup ocean-factory.ca

# OU
dig ocean-factory.ca
```

Vous devriez voir `rego-ocean-factory.onrender.com` ou l'IP de Render.

---

### 1️⃣1️⃣ Configurer Azure AD

Une fois le domaine actif:

1. **Azure Portal**: https://portal.azure.com
2. **Azure Active Directory** → **App registrations**
3. Trouvez votre app: `0bf5e2d3-8bd8-4018-bb93-574036e9da92`
4. **Authentication** → **Add a platform** → **Web**
5. **Redirect URIs**, ajoutez:
   ```
   https://ocean-factory.ca/auth/microsoft/callback
   https://www.ocean-factory.ca/auth/microsoft/callback
   ```
6. **Implicit grant**: Cochez `ID tokens` et `Access tokens`
7. **Save**

---

### 1️⃣2️⃣ Tester OAuth Microsoft!

1. Allez sur: `https://ocean-factory.ca`
2. Cliquez **Se connecter avec Microsoft**
3. Connectez-vous avec votre compte Microsoft
4. Vous devriez être redirigé vers le dashboard RegO!

---

## ✅ Checklist Finale

- [ ] Compte Render créé
- [ ] Code déployé (GitHub ou manuel)
- [ ] Variables d'environnement configurées
- [ ] App accessible sur `*.onrender.com`
- [ ] Domaine personnalisé ajouté dans Render
- [ ] DNS configuré dans GoDaddy
- [ ] DNS propagé (nslookup fonctionne)
- [ ] Azure AD redirect URI configuré
- [ ] OAuth Microsoft testé et fonctionne
- [ ] Synchronisation emails testée
- [ ] Export PDF testé

---

## 🔧 Commandes Utiles

### Générer clé secrète:
```bash
openssl rand -hex 32
```

### Créer repo Git local:
```bash
cd /Users/morelsttevensndong/RegO
git init
git add .
git commit -m "Deploy RegO to Render"
```

### Vérifier DNS:
```bash
nslookup ocean-factory.ca
dig ocean-factory.ca
```

### Voir les logs Render:
- Dashboard Render → Votre service → **Logs**
- Logs en temps réel automatiques!

---

## 🚨 Dépannage

### App ne démarre pas?
- Vérifiez les **logs** dans Render Dashboard
- Erreur commune: Variables d'environnement manquantes

### Domaine ne marche pas?
- Vérifiez la propagation DNS: `nslookup ocean-factory.ca`
- Attendez jusqu'à 30 min (parfois 24h)
- Vérifiez que le CNAME pointe vers `*.onrender.com`

### OAuth ne marche pas?
- Vérifiez que le redirect URI est bien dans Azure AD
- Format exact: `https://ocean-factory.ca/auth/microsoft/callback`
- HTTPS requis (Render gère automatiquement)

### "Application Error"?
```bash
# Vérifiez les logs Render
# Problème commun: MICROSOFT_CLIENT_SECRET manquant ou incorrect
```

---

## 💰 Coûts

**Plan Free (Gratuit):**
- ✅ 750h/mois (suffisant pour tester)
- ❌ Se met en veille après 15 min d'inactivité
- ❌ Redémarre lent (30s)

**Plan Starter (7$/mois):**
- ✅ Toujours actif
- ✅ Démarrage instantané
- ✅ 512MB RAM
- ✅ SSL automatique
- ✅ Domaine personnalisé

---

## 📞 Étapes Suivantes

**Maintenant:**
1. Créez compte Render: https://render.com
2. Uploadez/connectez le code RegO
3. Configurez variables d'environnement
4. Ajoutez domaine
5. Configurez DNS GoDaddy

**Je suis là pour vous aider à chaque étape!** 🚀

Dites-moi quand vous êtes prêt pour l'étape suivante!
