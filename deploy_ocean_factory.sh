#!/bin/bash

# ============================================
# Script de déploiement RegO sur ocean-factory.ca
# ============================================

set -e  # Arrêter en cas d'erreur

echo "🚀 Déploiement de RegO sur ocean-factory.ca"
echo "============================================"

# Vérifier qu'on est root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Ce script doit être exécuté en tant que root (sudo)"
    exit 1
fi

# Variables
APP_DIR="/var/www/ocean-factory.ca/RegO"
DOMAIN="ocean-factory.ca"
EMAIL="info@misterdil.ca"

echo ""
echo "📦 Étape 1: Installation des dépendances système"
apt-get update
apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git

echo ""
echo "📁 Étape 2: Création des répertoires"
mkdir -p /var/www/ocean-factory.ca
mkdir -p /var/log/rego
chown -R www-data:www-data /var/log/rego

echo ""
echo "📥 Étape 3: Clone/Mise à jour du code"
if [ -d "$APP_DIR" ]; then
    echo "Mise à jour du code existant..."
    cd "$APP_DIR"
    git pull
else
    echo "Clone du repository..."
    cd /var/www/ocean-factory.ca
    # Remplacez par votre repo
    # git clone https://github.com/votre-username/RegO.git
    echo "⚠️  Veuillez cloner manuellement votre repo dans $APP_DIR"
    echo "Puis relancez ce script"
    exit 1
fi

cd "$APP_DIR"

echo ""
echo "🐍 Étape 4: Configuration Python"
python3 -m venv venv
source venv/bin/activate

echo ""
echo "📚 Étape 5: Installation des packages Python"
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

echo ""
echo "⚙️  Étape 6: Configuration de l'environnement"
if [ ! -f "$APP_DIR/.env" ]; then
    echo "Copie de .env.production vers .env"
    cp .env.production .env
    
    # Générer une SECRET_KEY aléatoire
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    sed -i "s/CHANGEZ_CETTE_CLE_AVEC_UNE_VRAIMENT_ALEATOIRE_32_CHARS_MIN/$SECRET_KEY/" .env
    
    echo "✅ Fichier .env créé avec SECRET_KEY générée"
    echo "⚠️  IMPORTANT: Vérifiez et ajustez les valeurs dans $APP_DIR/.env"
else
    echo "✅ Fichier .env existe déjà"
fi

echo ""
echo "🗄️  Étape 7: Initialisation de la base de données"
python3 migrate_db.py

echo ""
echo "🌐 Étape 8: Configuration Nginx"
cat > /etc/nginx/sites-available/ocean-factory.ca <<'EOF'
server {
    listen 80;
    server_name ocean-factory.ca www.ocean-factory.ca;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ocean-factory.ca www.ocean-factory.ca;
    
    # Les certificats seront créés par Certbot
    ssl_certificate /etc/letsencrypt/live/ocean-factory.ca/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ocean-factory.ca/privkey.pem;
    
    # Configuration SSL moderne
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    
    # Headers de sécurité
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # Logs
    access_log /var/log/nginx/ocean-factory.access.log;
    error_log /var/log/nginx/ocean-factory.error.log;
    
    # Proxy vers Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts pour OAuth callbacks
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Fichiers statiques
    location /static {
        alias /var/www/ocean-factory.ca/RegO/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Limite de taille upload
    client_max_body_size 10M;
}
EOF

# Activer le site
ln -sf /etc/nginx/sites-available/ocean-factory.ca /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Tester la config Nginx
nginx -t

echo ""
echo "🔒 Étape 9: Configuration SSL avec Let's Encrypt"
echo "⚠️  Assurez-vous que le DNS de ocean-factory.ca pointe vers ce serveur!"
read -p "Voulez-vous configurer SSL maintenant? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    certbot --nginx -d ocean-factory.ca -d www.ocean-factory.ca --non-interactive --agree-tos --email $EMAIL
else
    echo "⚠️  Configurez SSL plus tard avec: sudo certbot --nginx -d ocean-factory.ca"
fi

echo ""
echo "🔧 Étape 10: Configuration du service systemd"
cat > /etc/systemd/system/rego.service <<EOF
[Unit]
Description=RegO Application - ocean-factory.ca
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn \\
    --workers 4 \\
    --worker-class sync \\
    --bind 127.0.0.1:8000 \\
    --timeout 120 \\
    --access-logfile /var/log/rego/access.log \\
    --error-logfile /var/log/rego/error.log \\
    --log-level info \\
    app_pro:app

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Permissions
chown -R www-data:www-data $APP_DIR

echo ""
echo "🚀 Étape 11: Démarrage des services"
systemctl daemon-reload
systemctl enable rego
systemctl restart rego
systemctl restart nginx

echo ""
echo "✅ Déploiement terminé!"
echo ""
echo "============================================"
echo "📊 État des services:"
echo "============================================"
systemctl status rego --no-pager
echo ""
systemctl status nginx --no-pager
echo ""
echo "============================================"
echo "🎉 RegO est maintenant accessible sur:"
echo "   https://ocean-factory.ca"
echo "============================================"
echo ""
echo "📝 Prochaines étapes:"
echo "1. Configurez Azure AD avec le Redirect URI:"
echo "   https://ocean-factory.ca/auth/microsoft/callback"
echo ""
echo "2. Testez la connexion:"
echo "   https://ocean-factory.ca/login"
echo ""
echo "3. Logs:"
echo "   - Application: tail -f /var/log/rego/error.log"
echo "   - Nginx: tail -f /var/log/nginx/ocean-factory.error.log"
echo ""
echo "4. Commandes utiles:"
echo "   - Redémarrer: sudo systemctl restart rego"
echo "   - Voir logs: sudo journalctl -u rego -f"
echo "   - Status: sudo systemctl status rego"
echo ""
