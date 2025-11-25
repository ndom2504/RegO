# 🎨 RegO - Dashboard Web

## 🎉 Nouveau! Interface Web avec Dashboard

RegO dispose maintenant d'une **interface web moderne et intuitive** avec un dashboard complet!

## 🚀 Lancement rapide

```bash
# Lancer le dashboard web
python app.py
```

Puis ouvrez votre navigateur sur: **http://localhost:5000**

## ✨ Fonctionnalités du Dashboard

### 📊 Statistiques en temps réel
- Total d'emails
- Emails non lus
- Emails avec pièces jointes
- Emails importants

### 🎛️ Actions disponibles
- **🔐 S'authentifier** - Connexion à votre compte Outlook
- **📥 Récupérer les emails** - Importer vos emails (avec choix du nombre)
- **📄 Exporter en PDF** - Générer un PDF professionnel
- **🗑️ Effacer le registre** - Nettoyer le registre
- **🔄 Rafraîchir** - Mettre à jour les données

### 📧 Liste des emails
- Affichage détaillé de chaque email
- Badges visuels (lu/non lu, pièces jointes, important)
- Aperçu du contenu
- Informations de l'expéditeur et date

### 🎨 Design moderne
- Interface responsive
- Animations fluides
- Notifications en temps réel
- Couleurs et icônes intuitives

## 📱 Interface vs Ligne de commande

### Dashboard Web (NOUVEAU) ⭐
```bash
python app.py
# Ouvrir http://localhost:5000
```
**Avantages:**
- ✅ Interface visuelle moderne
- ✅ Statistiques en temps réel
- ✅ Facile à utiliser
- ✅ Accessible depuis n'importe quel navigateur
- ✅ Parfait pour une utilisation quotidienne

### Ligne de commande (Classique)
```bash
python main.py
```
**Avantages:**
- ✅ Idéal pour les scripts automatisés
- ✅ Utilisation en SSH sur serveur
- ✅ Pas besoin de navigateur

## 🖥️ Captures d'écran du Dashboard

Le dashboard comprend:

1. **En-tête** - Status d'authentification et email configuré
2. **Cartes de statistiques** - Vue d'ensemble rapide
3. **Boutons d'action** - Toutes les fonctionnalités accessibles
4. **Liste des emails** - Affichage détaillé et scroll infini

## 🔧 Configuration

Même configuration que l'application CLI:

1. Fichier `.env` configuré
2. Identifiants Azure AD valides
3. Email configuré (`USER_EMAIL`)

## 🌐 Déploiement sur serveur

### En local
```bash
python app.py
# Accessible sur http://localhost:5000
```

### Sur serveur (accessible depuis l'extérieur)
```bash
# L'application écoute déjà sur 0.0.0.0:5000
# Configurez votre firewall pour autoriser le port 5000
```

### Avec Nginx (production)
```nginx
server {
    listen 80;
    server_name votredomaine.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔒 Sécurité

⚠️ **Important en production:**
- Désactivez le mode debug: `app.run(debug=False)`
- Utilisez HTTPS (certificat SSL)
- Ajoutez une authentification utilisateur
- Limitez l'accès par IP si nécessaire

## 📝 API Endpoints disponibles

- `GET /` - Page du dashboard
- `GET /api/status` - État de l'application
- `POST /api/authenticate` - Authentification
- `POST /api/fetch-emails` - Récupérer les emails
- `GET /api/emails` - Liste des emails
- `POST /api/export-pdf` - Générer un PDF
- `GET /api/download-pdf/<filename>` - Télécharger un PDF
- `POST /api/clear-registry` - Effacer le registre
- `GET /api/stats` - Statistiques détaillées

## 🎯 Utilisation typique

1. **Démarrage**
   ```bash
   python app.py
   ```

2. **Ouvrir le dashboard**
   - http://localhost:5000

3. **S'authentifier**
   - Cliquer sur "🔐 S'authentifier"

4. **Récupérer les emails**
   - Cliquer sur "📥 Récupérer les emails"
   - Choisir le nombre (ex: 100)
   - Valider

5. **Voir les emails**
   - Scroll dans la liste
   - Voir les détails de chaque email

6. **Exporter en PDF**
   - Cliquer sur "📄 Exporter en PDF"
   - Le téléchargement démarre automatiquement

## 🆚 Comparaison des interfaces

| Fonctionnalité | Dashboard Web | CLI |
|----------------|---------------|-----|
| Interface graphique | ✅ | ❌ |
| Statistiques visuelles | ✅ | ✅ |
| Navigation intuitive | ✅ | ❌ |
| Utilisation à distance | ✅ | ✅ |
| Scripts automatisés | ⚠️ | ✅ |
| Démo clients | ✅ | ❌ |

## 💡 Conseils

- **Utilisez le dashboard web** pour la gestion quotidienne
- **Utilisez le CLI** pour l'automatisation et les scripts
- **Les deux peuvent coexister** sans problème
- Le registre est partagé entre les deux interfaces

## 🔄 Mise à jour

Pour basculer entre les interfaces:

```bash
# Arrêter le dashboard (Ctrl+C)
# Lancer le CLI
python main.py

# Ou vice-versa
python app.py
```

---

**Le dashboard est maintenant votre interface principale pour RegO!** 🎉
