# 🎯 Déploiement Render - Actions Maintenant

## ✅ Préparation Terminée!

Voici ce qui est prêt:
- ✅ `requirements.txt` mis à jour (gunicorn + authlib)
- ✅ `FLASK_SECRET_KEY` générée: `77831fb56cc4f6dc5721c0a70bb6c84d7a825c511154820954612c7fa7e48613`
- ✅ `.gitignore` configuré
- ✅ Dockerfile créé (au cas où)

---

## 🚀 Vos Prochaines Étapes (15 minutes)

### ⏰ Maintenant - Étape 1: Créer compte Render (2 min)

1. **Ouvrez**: https://render.com
2. **Get Started for Free**
3. Inscrivez-vous avec:
   - **GitHub** (recommandé) OU
   - Email

---

### ⏰ Étape 2: Préparer le code pour upload (3 min)

**Option A - Via GitHub (Recommandé):**

```bash
cd /Users/morelsttevensndong/RegO

# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Commit
git commit -m "Initial commit - RegO pour ocean-factory.ca"

# Créez un repo sur GitHub puis:
git remote add origin https://github.com/[VOTRE-USERNAME]/RegO.git
git branch -M main
git push -u origin main
```

**Option B - Upload Manuel (Si pas de GitHub):**
- Compressez le dossier RegO en .zip
- Render accepte aussi les repos Git publics

---

### ⏰ Étape 3: Créer Web Service sur Render (5 min)

1. **Dashboard Render** → **New +** → **Web Service**

2. **Connectez le repo:**
   - Si GitHub: Sélectionnez le repo RegO
   - Sinon: Public Git Repository

3. **Configuration:**

**Name:** `rego-ocean-factory`

**Region:** `Oregon (US West)`

**Branch:** `main`

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn app_pro:app
```

**Instance Type:** 
- Free (pour tester)
- OU Starter - $7/mois (recommandé pour production)

---

### ⏰ Étape 4: Variables d'environnement (2 min)

Descendez à **Environment Variables** et ajoutez:

```
FLASK_SECRET_KEY
77831fb56cc4f6dc5721c0a70bb6c84d7a825c511154820954612c7fa7e48613

MICROSOFT_CLIENT_ID
0bf5e2d3-8bd8-4018-bb93-574036e9da92

MICROSOFT_CLIENT_SECRET
[VOTRE_SECRET_AZURE - voir ci-dessous]

MICROSOFT_TENANT_ID
common
```

**⚠️ MICROSOFT_CLIENT_SECRET:**
1. Allez sur: https://portal.azure.com
2. Azure Active Directory → App registrations
3. Votre app → Certificates & secrets
4. New client secret → Copiez la valeur
5. Collez dans Render

---

### ⏰ Étape 5: Déployer! (3 min)

1. **Cliquez "Create Web Service"**

2. **Attendez** le build (3-5 min)

3. **Vous verrez:**
   - 🔨 Installing dependencies...
   - ✅ Build successful
   - 🚀 Service live at: `https://rego-ocean-factory.onrender.com`

4. **Testez:** Ouvrez l'URL donnée

---

## 📱 Étapes Suivantes (Après déploiement)

### 6️⃣ Ajouter domaine personnalisé

**Dans Render Dashboard:**
- Settings → Custom Domain
- Add: `ocean-factory.ca`
- Render vous donne: `rego-ocean-factory.onrender.com`

### 7️⃣ Configurer DNS GoDaddy

**Dans GoDaddy:**

```
Type: CNAME
Name: @
Value: rego-ocean-factory.onrender.com
TTL: 600

Type: CNAME  
Name: www
Value: rego-ocean-factory.onrender.com
TTL: 600
```

### 8️⃣ Configurer Azure AD

**Dans Azure Portal:**

Redirect URIs:
```
https://ocean-factory.ca/auth/microsoft/callback
https://www.ocean-factory.ca/auth/microsoft/callback
```

---

## 🎯 Checklist Immédiate

**À FAIRE MAINTENANT:**

- [ ] Créer compte sur Render.com
- [ ] Décider: GitHub OU Upload manuel?
- [ ] Si GitHub: Pusher le code
- [ ] Créer Web Service sur Render
- [ ] Récupérer MICROSOFT_CLIENT_SECRET d'Azure
- [ ] Ajouter les 4 variables d'environnement
- [ ] Cliquer "Create Web Service"
- [ ] Attendre le déploiement
- [ ] Tester l'URL `.onrender.com`

**ENSUITE (10-30 min d'attente DNS):**

- [ ] Ajouter domaine personnalisé
- [ ] Configurer DNS GoDaddy
- [ ] Attendre propagation DNS
- [ ] Configurer Azure AD redirect URI
- [ ] Tester OAuth sur ocean-factory.ca
- [ ] 🎉 C'EST EN LIGNE!

---

## 📞 Besoin d'aide?

**Dites-moi où vous en êtes:**

1. "J'ai créé le compte Render" → Je vous guide pour le Web Service
2. "Le service est créé" → Je vous aide avec le domaine
3. "J'ai une erreur" → Envoyez-moi les logs
4. "Ça marche!" → On configure Azure AD

**Commencez par créer le compte Render: https://render.com** 🚀

Puis dites-moi quand vous êtes prêt pour l'étape suivante!
