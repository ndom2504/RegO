#!/bin/bash

# 🚀 Script de déploiement automatique via API Render
# Ce script crée et configure automatiquement le service sur Render

set -e

echo "🚀 Déploiement automatique sur Render via API"
echo "=============================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

# Demander la clé API
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔑 Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Tapez votre clé API Render (elle ne s'affichera pas):"
read -s RENDER_API_KEY
echo ""

if [ -z "$RENDER_API_KEY" ]; then
    error "Clé API vide!"
    exit 1
fi

info "Clé API reçue (${#RENDER_API_KEY} caractères)"
echo ""

# Demander le Microsoft Client Secret
echo "Tapez votre MICROSOFT_CLIENT_SECRET (Azure AD):"
read -s MICROSOFT_CLIENT_SECRET
echo ""

if [ -z "$MICROSOFT_CLIENT_SECRET" ]; then
    error "Microsoft Client Secret vide!"
    exit 1
fi

info "Microsoft Client Secret reçu (${#MICROSOFT_CLIENT_SECRET} caractères)"
echo ""

# Demander l'URL du repo GitHub
echo "Entrez l'URL de votre repo GitHub (ex: https://github.com/username/RegO):"
read GITHUB_REPO_URL

if [ -z "$GITHUB_REPO_URL" ]; then
    error "URL du repo vide!"
    exit 1
fi

info "Repository: $GITHUB_REPO_URL"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Création du service sur Render"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Préparer le JSON pour créer le service
SERVICE_JSON=$(cat <<EOF
{
  "type": "web_service",
  "name": "rego-ocean-factory",
  "repo": "$GITHUB_REPO_URL",
  "autoDeploy": "yes",
  "branch": "main",
  "rootDir": "",
  "envVars": [
    {
      "key": "FLASK_SECRET_KEY",
      "value": "77831fb56cc4f6dc5721c0a70bb6c84d7a825c511154820954612c7fa7e48613"
    },
    {
      "key": "MICROSOFT_CLIENT_ID",
      "value": "0bf5e2d3-8bd8-4018-bb93-574036e9da92"
    },
    {
      "key": "MICROSOFT_CLIENT_SECRET",
      "value": "$MICROSOFT_CLIENT_SECRET"
    },
    {
      "key": "MICROSOFT_TENANT_ID",
      "value": "common"
    }
  ],
  "serviceDetails": {
    "env": "python",
    "buildCommand": "pip install -r requirements.txt",
    "startCommand": "gunicorn app_pro:app",
    "plan": "starter",
    "region": "oregon"
  }
}
EOF
)

info "Création du service web..."

# Créer le service via l'API Render
RESPONSE=$(curl -s -X POST https://api.render.com/v1/services \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$SERVICE_JSON")

# Vérifier la réponse
if echo "$RESPONSE" | grep -q "id"; then
    SERVICE_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4 | head -1)
    SERVICE_URL=$(echo "$RESPONSE" | grep -o '"url":"[^"]*"' | cut -d'"' -f4 | head -1)
    
    success "Service créé avec succès!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 Informations du service"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🆔 Service ID: $SERVICE_ID"
    echo "🌐 URL: $SERVICE_URL"
    echo ""
    info "Le déploiement va commencer automatiquement..."
    info "Cela prendra 3-5 minutes."
    echo ""
    echo "📊 Suivez le déploiement sur:"
    echo "   https://dashboard.render.com/web/$SERVICE_ID"
    echo ""
    
    # Attendre un peu puis vérifier le statut
    info "Vérification du statut dans 10 secondes..."
    sleep 10
    
    STATUS_RESPONSE=$(curl -s -X GET "https://api.render.com/v1/services/$SERVICE_ID" \
      -H "Authorization: Bearer $RENDER_API_KEY")
    
    if echo "$STATUS_RESPONSE" | grep -q "status"; then
        STATUS=$(echo "$STATUS_RESPONSE" | grep -o '"serviceDetails":{"status":"[^"]*"' | cut -d'"' -f6)
        success "Statut actuel: $STATUS"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎯 Prochaines étapes"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1️⃣  Attendez la fin du déploiement (3-5 min)"
    echo "2️⃣  Testez: $SERVICE_URL"
    echo "3️⃣  Ajoutez le domaine personnalisé:"
    echo "    → Dashboard Render → Settings → Custom Domain"
    echo "    → Ajoutez: ocean-factory.ca"
    echo "4️⃣  Configurez DNS GoDaddy avec les infos de Render"
    echo "5️⃣  Configurez Azure AD redirect URI:"
    echo "    → https://ocean-factory.ca/auth/microsoft/callback"
    echo ""
    success "Déploiement lancé! 🎉"
else
    error "Erreur lors de la création du service"
    echo ""
    echo "Réponse de l'API:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    echo ""
    warning "Vérifiez votre clé API et réessayez"
    exit 1
fi
