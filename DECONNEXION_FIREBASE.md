# 🔌 Déconnecter Firebase de ocean-factory.ca

## 🎯 Situation Actuelle

Le domaine `ocean-factory.ca` est actuellement lié à Firebase Hosting (page "Site Not Found" visible).

Pour installer RegO dessus, il faut:
1. Déconnecter Firebase
2. Pointer le DNS vers votre serveur
3. Déployer RegO

---

## 📋 Option 1: Utiliser Firebase Hosting (RECOMMANDÉ - Le plus simple!)

**Avantage**: Pas besoin de serveur VPS, Firebase gère tout (SSL, CDN, scaling)

### Étape 1: Configurer Firebase pour RegO

```bash
# Dans le dossier RegO
cd /Users/morelsttevensndong/RegO

# Installer Firebase CLI
npm install -g firebase-tools

# Login Firebase
firebase login

# Initialiser
firebase init hosting
```

**Répondez:**
- Projet: Sélectionnez le projet lié à ocean-factory.ca
- Public directory: `static` (ou créez un dossier pour les fichiers statiques)
- Single-page app: Non
- Automatic builds: Non

### Étape 2: Préparer RegO pour Firebase

Firebase Hosting ne peut pas héberger directement une app Flask. Vous avez 2 choix:

#### Option A: Firebase + Cloud Run (App Flask complète)
```bash
# Créer Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

CMD exec gunicorn --bind :$PORT --workers 4 app_pro:app
EOF

# Déployer sur Cloud Run
gcloud run deploy rego \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Connecter à Firebase
firebase hosting:channel:deploy production
```

#### Option B: Hébergeur Python + DNS (Plus simple pour commencer)
Utilisez Heroku, Render, ou Railway - voir Option 2 ci-dessous.

---

## 📋 Option 2: Déconnecter Firebase et utiliser un autre hébergeur

### Étape 1: Console Firebase
1. Allez sur: https://console.firebase.google.com
2. Sélectionnez votre projet
3. **Hosting** → **Domaines personnalisés**
4. Trouvez `ocean-factory.ca`
5. Cliquez **Supprimer** ou **Déconnecter**

### Étape 2: Changez les DNS

Allez chez votre registrar de domaine (GoDaddy, Namecheap, etc.):

**Supprimez les records actuels:**
```
Type: A ou CNAME pointant vers Firebase
```

**Ajoutez selon votre hébergeur:**

#### Pour un VPS (DigitalOcean, Linode, Vultr):
```
Type: A
Nom: @
Valeur: [IP de votre serveur]
TTL: 3600

Type: A
Nom: www
Valeur: [IP de votre serveur]
TTL: 3600
```

#### Pour Heroku:
```
Type: CNAME
Nom: www
Valeur: [votre-app].herokuapp.com
TTL: 3600

Type: ALIAS ou ANAME (si supporté)
Nom: @
Valeur: [votre-app].herokuapp.com
```

#### Pour Render.com:
```
Type: CNAME
Nom: @
Valeur: [votre-app].onrender.com
TTL: 3600
```

### Étape 3: Attendez la propagation DNS
```bash
# Vérifiez (peut prendre 5 min à 48h)
nslookup ocean-factory.ca
```

---

## 🚀 Option 3: Heroku (Le plus rapide!)

**Coût**: Gratuit pour commencer, 7$/mois pour production

### Setup complet:

```bash
cd /Users/morelsttevensndong/RegO

# Installer Heroku CLI
brew tap heroku/brew && brew install heroku

# Login
heroku login

# Créer app
heroku create rego-ocean-factory

# Ajouter Procfile
cat > Procfile << 'EOF'
web: gunicorn app_pro:app --log-file -
EOF

# Créer runtime.txt
echo "python-3.9.6" > runtime.txt

# Variables d'environnement
heroku config:set FLASK_SECRET_KEY=$(openssl rand -hex 32)
heroku config:set MICROSOFT_CLIENT_ID="0bf5e2d3-8bd8-4018-bb93-574036e9da92"
heroku config:set MICROSOFT_CLIENT_SECRET="[votre secret]"
heroku config:set MICROSOFT_TENANT_ID="common"

# Déployer
git add .
git commit -m "Deploy RegO to Heroku"
git push heroku main

# Connecter domaine
heroku domains:add ocean-factory.ca
heroku domains:add www.ocean-factory.ca
```

**Heroku vous donnera les DNS à configurer:**
```
www.ocean-factory.ca CNAME [quelquechose].herokudns.com
ocean-factory.ca ALIAS [quelquechose].herokudns.com
```

Copiez ces valeurs dans votre registrar de domaine!

---

## 🚀 Option 4: Render.com (Recommandé - Simple et moderne)

**Coût**: Gratuit pour commencer, 7$/mois pour production

### Setup:

1. Allez sur: https://render.com
2. **New** → **Web Service**
3. Connectez votre repo Git (ou uploadez le code)
4. Configuration:
   - Name: `rego-ocean-factory`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app_pro:app`
5. **Environment Variables**:
   ```
   FLASK_SECRET_KEY=[générez avec openssl rand -hex 32]
   MICROSOFT_CLIENT_ID=0bf5e2d3-8bd8-4018-bb93-574036e9da92
   MICROSOFT_CLIENT_SECRET=[votre secret]
   MICROSOFT_TENANT_ID=common
   ```
6. **Settings** → **Custom Domain**
7. Ajoutez: `ocean-factory.ca` et `www.ocean-factory.ca`
8. Copiez les records DNS fournis
9. Ajoutez-les chez votre registrar

**Render gère automatiquement le SSL avec Let's Encrypt!** ✅

---

## 🚀 Option 5: Railway.app (Ultra simple!)

**Coût**: 5$/mois

### Setup ultra-rapide:

```bash
cd /Users/morelsttevensndong/RegO

# Installer Railway CLI
brew install railway

# Login
railway login

# Init projet
railway init

# Ajouter variables
railway variables set FLASK_SECRET_KEY=$(openssl rand -hex 32)
railway variables set MICROSOFT_CLIENT_ID="0bf5e2d3-8bd8-4018-bb93-574036e9da92"
railway variables set MICROSOFT_CLIENT_SECRET="[votre secret]"
railway variables set MICROSOFT_TENANT_ID="common"

# Déployer
railway up

# Ajouter domaine
railway domain add ocean-factory.ca
```

Railway vous donne les DNS à configurer automatiquement!

---

## ⚡ Ma Recommandation

**Pour vous, je recommande Render.com:**

✅ **Pros:**
- Setup en 10 minutes
- SSL automatique
- Logs en temps réel
- 7$/mois (ou gratuit pour tester)
- Interface moderne
- Pas besoin de gérer Nginx/serveur

❌ **Cons:**
- Instance se met en veille après inactivité (plan gratuit)

### Étapes finales:

1. **Déconnectez Firebase**: Console Firebase → Hosting → Retirer ocean-factory.ca
2. **Créez compte Render**: https://render.com
3. **Uploadez RegO**: Git repo ou uploadez le dossier
4. **Configurez variables d'environnement**
5. **Ajoutez domaine personnalisé**: ocean-factory.ca
6. **Copiez DNS fournis par Render**
7. **Allez chez votre registrar** (GoDaddy, Namecheap, etc.)
8. **Changez les DNS** avec ceux de Render
9. **Attendez 5-30 minutes**
10. **Testez**: https://ocean-factory.ca ✅

---

## 🔍 Vérifier que Firebase est déconnecté

```bash
# Dig pour voir les DNS actuels
dig ocean-factory.ca

# Si vous voyez encore Firebase:
# - CNAME pointant vers firebase.com ou firebaseapp.com
# → Il faut changer les DNS chez votre registrar
```

---

## 📞 Besoin d'aide?

**Je peux vous guider étape par étape!**

Dites-moi:
1. Vous préférez quelle option? (Render, Heroku, Railway, VPS)
2. C'est vous qui gérez le domaine ocean-factory.ca? (accès au registrar?)
3. Vous voulez du gratuit d'abord ou directement production?

**Option la plus rapide: Render.com en 10 minutes!** 🚀
