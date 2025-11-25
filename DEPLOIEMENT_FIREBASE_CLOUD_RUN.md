# 🚀 Déploiement RegO sur Firebase + Cloud Run

## ✅ Fichiers créés:
- ✅ `Dockerfile` - Image Docker optimisée pour Cloud Run
- ✅ `.dockerignore` - Exclut fichiers inutiles
- ✅ `firebase.json` - Configuration Firebase Hosting
- ✅ `public/index.html` - Page de chargement

## 📋 Étapes de déploiement

### 1️⃣ Login Firebase
```bash
cd /Users/morelsttevensndong/RegO
firebase login
```

### 2️⃣ Associer au projet RegO
```bash
firebase use --add
# Sélectionnez votre projet "RegO" dans la liste
# Donnez-lui l'alias: production
```

### 3️⃣ Activer les services Google Cloud
```bash
# Ces commandes activent les APIs nécessaires
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 4️⃣ Créer les secrets pour les variables d'environnement
```bash
# Générer une clé secrète Flask
SECRET_KEY=$(openssl rand -hex 32)

# Créer les secrets dans Google Secret Manager
echo -n "$SECRET_KEY" | gcloud secrets create FLASK_SECRET_KEY --data-file=-
echo -n "0bf5e2d3-8bd8-4018-bb93-574036e9da92" | gcloud secrets create MICROSOFT_CLIENT_ID --data-file=-
echo -n "VOTRE_CLIENT_SECRET" | gcloud secrets create MICROSOFT_CLIENT_SECRET --data-file=-
echo -n "common" | gcloud secrets create MICROSOFT_TENANT_ID --data-file=-
```

### 5️⃣ Déployer sur Cloud Run
```bash
gcloud run deploy rego \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets="FLASK_SECRET_KEY=FLASK_SECRET_KEY:latest,MICROSOFT_CLIENT_ID=MICROSOFT_CLIENT_ID:latest,MICROSOFT_CLIENT_SECRET=MICROSOFT_CLIENT_SECRET:latest,MICROSOFT_TENANT_ID=MICROSOFT_TENANT_ID:latest"
```

### 6️⃣ Déployer Firebase Hosting
```bash
firebase deploy --only hosting
```

### 7️⃣ Connecter le domaine ocean-factory.ca

#### Dans Firebase Console:
1. **Hosting** → **Add custom domain**
2. Entrez: `ocean-factory.ca`
3. Firebase vous donnera des records DNS

#### Dans GoDaddy:
Remplacez vos records DNS actuels par ceux de Firebase:

**Supprimez:**
- Les NS records `ns15.domaincontrol.com` et `ns16.domaincontrol.com` (gardez-les si c'est les nameservers principaux)
- Le CNAME `_domainconnect`

**Ajoutez les records donnés par Firebase:**
- Type: **A** → Nom: **@** → Valeur: **[IP Firebase]**
- Type: **A** → Nom: **www** → Valeur: **[IP Firebase]**
- Type: **TXT** → Nom: **@** → Valeur: **[Verification Firebase]**

### 8️⃣ Configurer Azure AD

Ajoutez ces redirect URIs dans Azure Portal:
```
https://ocean-factory.ca/auth/microsoft/callback
https://www.ocean-factory.ca/auth/microsoft/callback
```

---

## 🎯 Commandes Rapides (Tout en une fois)

```bash
#!/bin/bash
cd /Users/morelsttevensndong/RegO

# 1. Login
firebase login

# 2. Associer projet
firebase use --add

# 3. Activer APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com secretmanager.googleapis.com

# 4. Créer secrets
SECRET_KEY=$(openssl rand -hex 32)
echo -n "$SECRET_KEY" | gcloud secrets create FLASK_SECRET_KEY --data-file=- --replication-policy=automatic
echo -n "0bf5e2d3-8bd8-4018-bb93-574036e9da92" | gcloud secrets create MICROSOFT_CLIENT_ID --data-file=- --replication-policy=automatic
echo -n "VOTRE_CLIENT_SECRET_ICI" | gcloud secrets create MICROSOFT_CLIENT_SECRET --data-file=- --replication-policy=automatic
echo -n "common" | gcloud secrets create MICROSOFT_TENANT_ID --data-file=- --replication-policy=automatic

# 5. Déployer Cloud Run
gcloud run deploy rego \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets="FLASK_SECRET_KEY=FLASK_SECRET_KEY:latest,MICROSOFT_CLIENT_ID=MICROSOFT_CLIENT_ID:latest,MICROSOFT_CLIENT_SECRET=MICROSOFT_CLIENT_SECRET:latest,MICROSOFT_TENANT_ID=MICROSOFT_TENANT_ID:latest"

# 6. Déployer Firebase Hosting
firebase deploy --only hosting

echo "✅ Déploiement terminé!"
echo "🌐 Visitez: https://[votre-projet].web.app"
echo "📝 Maintenant, ajoutez votre domaine personnalisé dans Firebase Console"
```

---

## 🔍 Vérifications

### Tester Cloud Run:
```bash
# Obtenir l'URL Cloud Run
gcloud run services describe rego --region=us-central1 --format='value(status.url)'

# Tester
curl https://[URL-CLOUD-RUN]/
```

### Tester Firebase Hosting:
```bash
# Ouvrir dans le navigateur
firebase open hosting:site
```

### Voir les logs:
```bash
# Logs Cloud Run
gcloud run services logs read rego --region=us-central1

# Logs Firebase Hosting
firebase hosting:logs
```

---

## 💰 Coûts

- **Firebase Hosting**: GRATUIT (10 GB/mois)
- **Cloud Run**: GRATUIT jusqu'à 2M requêtes/mois
- **Cloud Build**: GRATUIT (120 min/jour)
- **Secret Manager**: GRATUIT (6 secrets)

**Total: 0$ pour commencer!** 🎉

---

## ⚠️ Important

1. **Client Secret Microsoft**: Remplacez `VOTRE_CLIENT_SECRET_ICI` par votre vrai secret Azure AD
2. **DNS GoDaddy**: Attendez 5-30 min pour la propagation
3. **SSL**: Firebase gère automatiquement le certificat SSL
4. **Base de données**: SQLite ne persiste pas sur Cloud Run. Pour production, utilisez Cloud SQL ou Firestore.

---

## 🎯 Prochaines étapes

Une fois déployé:
1. ✅ Tester https://ocean-factory.ca/login
2. ✅ Cliquer "Se connecter avec Microsoft"
3. ✅ Vérifier la synchronisation des emails
4. ✅ Exporter un PDF

**Votre RegO sera en ligne sur ocean-factory.ca!** 🚀
