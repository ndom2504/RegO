#!/bin/bash

# 🚀 Déploiement RegO - Méthode Simple SANS API
# Ce script prépare tout et vous guide vers l'interface Render

set -e

echo "🚀 Préparation pour déploiement Render (SANS API)"
echo "=================================================="
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

cd /Users/morelsttevensndong/RegO

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 ÉTAPE 1: Configuration Git"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Configurer Git si nécessaire
if ! git config user.name > /dev/null 2>&1; then
    info "Configuration Git..."
    git config --global user.name "Morel Stevens Ndong"
    git config --global user.email "morelstevensndong@gmail.com"
    success "Git configuré"
fi

echo "Votre nom GitHub: $(git config user.name)"
echo "Votre email: $(git config user.email)"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 ÉTAPE 2: Créer repo GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

info "Ouverture de GitHub dans votre navigateur..."
sleep 1
open "https://github.com/new"

echo ""
echo "Sur GitHub:"
echo "  1. Repository name: ${BLUE}RegO${NC}"
echo "  2. Description: Email registry with Microsoft OAuth"
echo "  3. Public ou Private: ${BLUE}au choix${NC}"
echo "  4. ${YELLOW}N'ajoutez RIEN${NC} (pas de README, .gitignore, etc.)"
echo "  5. Cliquez ${GREEN}Create repository${NC}"
echo ""

read -p "Appuyez sur ENTRÉE quand le repo est créé..."

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔗 ÉTAPE 3: Lier au repo GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Entrez votre username GitHub:"
read GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    warning "Username vide, utilisation de 'morelsttevensndong'"
    GITHUB_USERNAME="morelsttevensndong"
fi

REPO_URL="https://github.com/$GITHUB_USERNAME/RegO.git"

info "URL du repo: $REPO_URL"
echo ""

# Vérifier si remote existe déjà
if git remote get-url origin > /dev/null 2>&1; then
    warning "Remote 'origin' existe déjà, suppression..."
    git remote remove origin
fi

info "Ajout du remote..."
git remote add origin "$REPO_URL"
success "Remote ajouté"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⬆️  ÉTAPE 4: Push vers GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

info "Push du code vers GitHub..."
git branch -M main

if git push -u origin main; then
    success "Code poussé sur GitHub avec succès! 🎉"
else
    warning "Erreur lors du push. Si demandé, connectez-vous à GitHub."
    info "Si vous utilisez 2FA, créez un Personal Access Token:"
    info "  → https://github.com/settings/tokens"
    info "  → Generate new token (classic)"
    info "  → Cochez: repo (toutes les cases)"
    info "  → Utilisez ce token comme mot de passe"
    echo ""
    read -p "Appuyez sur ENTRÉE pour réessayer le push..."
    git push -u origin main
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 ÉTAPE 5: Déployer sur Render"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

BLUEPRINT_URL="https://render.com/deploy?repo=https://github.com/$GITHUB_USERNAME/RegO"

success "Code prêt pour le déploiement!"
echo ""
echo "Méthode 1 - Blueprint (1 CLIC!) ⭐ RECOMMANDÉ:"
echo ""
echo "  Cliquez sur ce lien (ou copiez dans votre navigateur):"
echo "  ${GREEN}$BLUEPRINT_URL${NC}"
echo ""
info "Ouverture automatique dans 3 secondes..."
sleep 3
open "$BLUEPRINT_URL"

echo ""
echo "Méthode 2 - Manuelle (si Blueprint ne marche pas):"
echo ""
echo "  1. Allez sur: https://dashboard.render.com"
echo "  2. New + → Web Service"
echo "  3. Connect GitHub repository"
echo "  4. Sélectionnez: RegO"
echo "  5. Render va détecter render.yaml automatiquement! ✨"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 ÉTAPE 6: Ajouter le secret Microsoft"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

warning "IMPORTANT: Render va vous demander 1 variable manquante!"
echo ""
echo "  Variable: ${BLUE}MICROSOFT_CLIENT_SECRET${NC}"
echo ""
echo "  Pour l'obtenir:"
echo "  1. Allez sur: https://portal.azure.com"
echo "  2. Azure Active Directory → App registrations"
echo "  3. Votre app: 0bf5e2d3-8bd8-4018-bb93-574036e9da92"
echo "  4. Certificates & secrets → New client secret"
echo "  5. Add → COPIEZ la valeur"
echo "  6. Collez dans Render"
echo ""

info "Ouverture d'Azure Portal dans 3 secondes..."
sleep 3
open "https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Credentials/appId/0bf5e2d3-8bd8-4018-bb93-574036e9da92"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ RÉSUMÉ - Ce qui va se passer sur Render:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Render va automatiquement:"
echo "  ✅ Détecter Python 3"
echo "  ✅ Installer: pip install -r requirements.txt"
echo "  ✅ Démarrer: gunicorn app_pro:app"
echo "  ✅ Configurer les variables (depuis render.yaml):"
echo "     • FLASK_SECRET_KEY ✅"
echo "     • MICROSOFT_CLIENT_ID ✅"
echo "     • MICROSOFT_TENANT_ID ✅"
echo ""
echo "Vous devez ajouter UNIQUEMENT:"
echo "  🔑 MICROSOFT_CLIENT_SECRET (d'Azure)"
echo ""
echo "Temps de déploiement: ${YELLOW}3-5 minutes${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 Après le déploiement:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Testez l'URL donnée (ex: rego-ocean-factory.onrender.com)"
echo "2. Ajoutez votre domaine: Settings → Custom Domain → ocean-factory.ca"
echo "3. Configurez DNS GoDaddy avec les infos de Render"
echo "4. Ajoutez redirect URI dans Azure AD:"
echo "   → https://ocean-factory.ca/auth/microsoft/callback"
echo ""

success "Tout est prêt! Suivez les étapes sur Render. 🚀"
echo ""
