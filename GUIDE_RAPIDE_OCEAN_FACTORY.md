# 🌊 Guide Rapide: RegO sur ocean-factory.ca

## 📋 Résumé en 3 étapes

### 1️⃣ Configurer Azure AD (5 minutes)

Allez sur: https://portal.azure.com

```
Azure Active Directory
→ App registrations  
→ Votre app: 0bf5e2d3-8bd8-4018-bb93-574036e9da92
→ Authentication
→ Add Redirect URI:
```

**Ajoutez ces URLs:**
```
✅ https://ocean-factory.ca/auth/microsoft/callback
✅ https://www.ocean-factory.ca/auth/microsoft/callback
✅ http://localhost:5000/auth/microsoft/callback (pour tests)
```

**Cochez:**
- ✅ Access tokens
- ✅ ID tokens

**Save!**

---

### 2️⃣ Déployer sur votre serveur (10 minutes)

**Sur votre serveur ocean-factory.ca:**

```bash
# Connectez-vous en SSH
ssh root@ocean-factory.ca

# Téléchargez le script
wget https://raw.githubusercontent.com/[votre-repo]/deploy_ocean_factory.sh
# OU transférez le fichier avec scp:
# scp deploy_ocean_factory.sh root@ocean-factory.ca:/root/

# Exécutez
chmod +x deploy_ocean_factory.sh
sudo ./deploy_ocean_factory.sh
```

Le script fait TOUT automatiquement:
- ✅ Installe Python, Nginx, etc.
- ✅ Configure SSL avec Let's Encrypt
- ✅ Démarre l'application
- ✅ Configure le service systemd

---

### 3️⃣ Tester! (2 minutes)

**Ouvrez:** https://ocean-factory.ca/login

**Cliquez sur:** "Se connecter avec Microsoft"

**C'EST TOUT!** 🎉

---

## 🔧 Configuration Manuelle (Alternative)

Si vous préférez tout faire vous-même:

### Sur votre serveur:

```bash
# 1. Installer
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# 2. Cloner le code
cd /var/www
git clone [votre-repo] ocean-factory.ca
cd ocean-factory.ca/RegO

# 3. Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 4. Configuration
cp .env.production .env
# Éditez .env et changez SECRET_KEY

# 5. Base de données
python3 migrate_db.py

# 6. SSL
sudo certbot --nginx -d ocean-factory.ca -d www.ocean-factory.ca

# 7. Démarrer
sudo systemctl start rego
sudo systemctl enable rego
```

---

## 📊 Commandes Utiles

### Voir les logs:
```bash
# Logs application
tail -f /var/log/rego/error.log

# Logs Nginx
tail -f /var/log/nginx/ocean-factory.error.log

# Logs système
sudo journalctl -u rego -f
```

### Redémarrer:
```bash
sudo systemctl restart rego
sudo systemctl restart nginx
```

### Status:
```bash
sudo systemctl status rego
sudo systemctl status nginx
```

---

## 🚨 Troubleshooting

### L'app ne démarre pas?
```bash
# Vérifiez les logs
sudo journalctl -u rego -n 50
```

### Erreur 502 Bad Gateway?
```bash
# L'app ne tourne pas
sudo systemctl start rego
```

### OAuth ne marche pas?
```bash
# Vérifiez Azure AD:
# 1. Redirect URI configuré?
# 2. HTTPS activé?
# 3. Certificat SSL valide?
```

---

## 💰 Coûts

- **Serveur VPS**: ~6$/mois (DigitalOcean, Linode, Vultr)
- **Domaine ocean-factory.ca**: Vous l'avez déjà! ✅
- **SSL**: GRATUIT (Let's Encrypt) ✅
- **Azure AD**: GRATUIT ✅

**Total: 6$/mois** 🎉

---

## 🎯 URLs Importantes

| Service | URL |
|---------|-----|
| **Application** | https://ocean-factory.ca |
| **Login** | https://ocean-factory.ca/login |
| **Dashboard** | https://ocean-factory.ca/dashboard |
| **Azure AD** | https://portal.azure.com |

---

## ✅ Checklist Pré-Déploiement

- [ ] Serveur avec Ubuntu/Debian accessible en SSH
- [ ] DNS de ocean-factory.ca pointe vers le serveur
- [ ] Ports 80 et 443 ouverts sur le firewall
- [ ] Azure AD Redirect URI configuré
- [ ] Code RegO prêt (avec .env.production)

---

## 🚀 Lancer en 1 commande

```bash
ssh root@ocean-factory.ca 'bash -s' < deploy_ocean_factory.sh
```

**Fait!** Votre RegO est en ligne! 🎊

---

## 📞 Support

Problème? Vérifiez:
1. `DEPLOIEMENT_OCEAN_FACTORY.md` - Guide détaillé
2. `CONFIGURATION_AZURE.md` - Config Azure AD
3. Logs: `/var/log/rego/error.log`

**Bon déploiement!** 🚀
