# ⚠️ Facturation Google Cloud Requise

## Problème
Pour utiliser Cloud Run, il faut activer la facturation sur votre projet Firebase/Google Cloud.

## ✅ Solution Rapide

### Option 1: Activer la facturation (RECOMMANDÉ)

1. **Allez sur**: https://console.cloud.google.com/billing/linkedaccount?project=rego-c452d

2. **Liez un compte de facturation**:
   - Si vous en avez déjà un: Sélectionnez-le
   - Sinon: Créez-en un nouveau (carte de crédit requise)

3. **Gratuit pour commencer!**
   - Cloud Run: **2M requêtes gratuites/mois**
   - Cloud Build: **120 min/jour gratuit**
   - Secret Manager: **6 secrets gratuits**
   - Vous ne serez facturé que si vous dépassez ces limites

### Option 2: Utiliser un hébergeur sans carte de crédit

Si vous ne voulez pas donner de carte, utilisez plutôt **Render.com** ou **Heroku**:

#### Render.com (Simple et moderne)
```bash
# 1. Créez compte sur: https://render.com
# 2. New → Web Service
# 3. Connectez votre code
# 4. Configuration:
#    - Environment: Python 3
#    - Build: pip install -r requirements.txt
#    - Start: gunicorn app_pro:app
# 5. Variables d'environnement:
#    FLASK_SECRET_KEY=[générez avec: openssl rand -hex 32]
#    MICROSOFT_CLIENT_ID=0bf5e2d3-8bd8-4018-bb93-574036e9da92
#    MICROSOFT_CLIENT_SECRET=[votre secret Azure]
#    MICROSOFT_TENANT_ID=common
# 6. Ajoutez domaine: ocean-factory.ca
# 7. Copiez les DNS dans GoDaddy
```

**Coût Render**: 7$/mois (ou gratuit avec limitations)

#### Heroku
```bash
cd /Users/morelsttevensndong/RegO

# Installer Heroku CLI
brew tap heroku/brew && brew install heroku

# Login
heroku login

# Créer app
heroku create rego-ocean-factory

# Variables
heroku config:set FLASK_SECRET_KEY=$(openssl rand -hex 32)
heroku config:set MICROSOFT_CLIENT_ID="0bf5e2d3-8bd8-4018-bb93-574036e9da92"
heroku config:set MICROSOFT_CLIENT_SECRET="[votre secret]"
heroku config:set MICROSOFT_TENANT_ID="common"

# Créer Procfile
echo "web: gunicorn app_pro:app" > Procfile

# Déployer
git init
git add .
git commit -m "Deploy RegO"
git push heroku main

# Ajouter domaine
heroku domains:add ocean-factory.ca
heroku domains:add www.ocean-factory.ca
```

**Coût Heroku**: 7$/mois

---

## 📊 Comparaison

| Service | Carte requise? | Gratuit? | Coût/mois | Setup |
|---------|---------------|----------|-----------|-------|
| **Firebase + Cloud Run** | ✅ Oui | Oui (limité) | 0-10$ | Complexe |
| **Render.com** | ❌ Non (essai) | Oui (limité) | 0-7$ | Simple ✨ |
| **Heroku** | ❌ Non (essai) | Non | 7$ | Simple |
| **Railway** | ✅ Oui | 5$ crédit | 5$ | Ultra simple |

---

## 🎯 Ma Recommandation

**Pour vous → Render.com!**

Pourquoi?
- ✅ Pas de carte pour essayer
- ✅ Interface moderne et simple
- ✅ SSL automatique
- ✅ Domaine personnalisé facile
- ✅ Déploiement en 10 minutes

**Étapes Render:**

1. **Créez compte**: https://render.com (email seulement)
2. **New → Web Service**
3. **Upload votre code RegO**
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `gunicorn app_pro:app`
6. **Variables d'environnement** (copiez du .env)
7. **Deploy!**
8. **Add Custom Domain**: ocean-factory.ca
9. **Copiez les DNS dans GoDaddy**

**DNS GoDaddy pour Render:**
```
Type: CNAME
Nom: @
Valeur: [votre-app].onrender.com

Type: CNAME
Nom: www
Valeur: [votre-app].onrender.com
```

---

## 🔥 Si vous voulez vraiment Firebase

1. **Activez la facturation**: https://console.cloud.google.com/billing/linkedaccount?project=rego-c452d
2. **Ajoutez une carte de crédit**
3. **Ne vous inquiétez pas**: Vous ne serez pas facturé si vous restez dans les limites gratuites
4. **Revenez ici** et continuez le déploiement

---

## 💡 Prochaine Étape

**Dites-moi ce que vous préférez:**

A) J'active la facturation sur Firebase (j'ai une carte)
B) Je veux utiliser Render.com (pas de carte pour essayer)
C) Je veux utiliser Heroku (7$/mois)

Je vous guide étape par étape! 🚀
