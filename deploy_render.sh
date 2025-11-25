#!/bin/bash

# 🚀 Script de déploiement automatique sur Render.com
# Ce script automatise le déploiement de RegO sur Render

set -e  # Arrête en cas d'erreur

echo "🚀 Déploiement RegO sur Render.com"
echo "=================================="
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Vérifier si Git est installé
if ! command -v git &> /dev/null; then
    error "Git n'est pas installé. Installez-le avec: brew install git"
    exit 1
fi

info "Vérification du dossier..."
cd /Users/morelsttevensndong/RegO

# Vérifier si c'est déjà un repo Git
if [ ! -d .git ]; then
    info "Initialisation du repository Git..."
    git init
    success "Repository Git initialisé"
else
    success "Repository Git déjà initialisé"
fi

# Créer .gitignore s'il n'existe pas déjà
if [ ! -f .gitignore ]; then
    info "Création du .gitignore..."
    cat > .gitignore << 'EOF'
# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
ENV/

# Data files
rego.db
*.db
*.sqlite
*.sqlite3

# Export files
emails_pdf/*.pdf

# IDE
.vscode/
.idea/

# OS
.DS_Store

# Token cache
token_cache.bin
EOF
    success ".gitignore créé"
fi

# Ajouter tous les fichiers
info "Ajout des fichiers au repository..."
git add .

# Vérifier s'il y a des changements à commiter
if git diff-index --quiet HEAD --; then
    warning "Aucun changement à commiter"
else
    info "Commit des changements..."
    git commit -m "Deploy RegO to Render - $(date '+%Y-%m-%d %H:%M:%S')" || true
    success "Changements commités"
fi

echo ""
echo "=================================="
echo "📋 PROCHAINES ÉTAPES MANUELLES"
echo "=================================="
echo ""

echo "Vous avez 2 options pour déployer:"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔷 OPTION A: Via GitHub (Recommandé)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Créez un nouveau repository sur GitHub:"
echo "   https://github.com/new"
echo ""
echo "2️⃣  Nommez-le: RegO"
echo ""
echo "3️⃣  Puis exécutez ces commandes:"
echo ""
echo -e "${BLUE}git branch -M main"
echo "git remote add origin https://github.com/[VOTRE-USERNAME]/RegO.git"
echo "git push -u origin main${NC}"
echo ""
echo "4️⃣  Sur Render.com:"
echo "   → New → Web Service"
echo "   → Connect GitHub repository"
echo "   → Sélectionnez le repo RegO"
echo "   → Render détectera automatiquement render.yaml! ✨"
echo ""
echo "5️⃣  Ajoutez UNIQUEMENT cette variable:"
echo "   Key: MICROSOFT_CLIENT_SECRET"
echo "   Value: [Votre secret Azure]"
echo ""
echo "   Les autres variables sont déjà dans render.yaml!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔶 OPTION B: Blueprint Render (Plus rapide)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Créez un repo GitHub (voir Option A, étapes 1-3)"
echo ""
echo "2️⃣  Cliquez sur ce lien avec VOTRE repo:"
echo ""
echo -e "${GREEN}https://render.com/deploy?repo=https://github.com/[VOTRE-USERNAME]/RegO${NC}"
echo ""
echo "3️⃣  Render déploiera automatiquement avec render.yaml!"
echo ""
echo "4️⃣  Ajoutez MICROSOFT_CLIENT_SECRET dans les variables"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Récupérer MICROSOFT_CLIENT_SECRET"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Allez sur: https://portal.azure.com"
echo "2. Azure Active Directory → App registrations"
echo "3. Votre app: 0bf5e2d3-8bd8-4018-bb93-574036e9da92"
echo "4. Certificates & secrets → New client secret"
echo "5. COPIEZ la valeur immédiatement!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Fichiers créés:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ render.yaml - Configuration Render automatique"
echo "✅ .gitignore - Exclut fichiers sensibles"
echo "✅ Git repository initialisé"
echo "✅ Fichiers committes"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 Résumé rapide:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Créez repo GitHub"
echo "2. git push vers GitHub"
echo "3. Render.com → Connect GitHub repo"
echo "4. Ajoutez MICROSOFT_CLIENT_SECRET"
echo "5. Deploy! 🚀"
echo ""

success "Script terminé! Prêt pour le déploiement."
echo ""
