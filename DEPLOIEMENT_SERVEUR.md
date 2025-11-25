# Guide de déploiement sur serveur - RegO

Ce guide explique comment déployer et tester RegO sur un serveur distant.

## 📦 Prérequis serveur

- Python 3.8+ installé
- Accès SSH au serveur
- Git (optionnel, pour le déploiement)

## 🚀 Méthode 1: Déploiement via SSH et transfert de fichiers

### 1. Préparer le projet localement

```bash
# Créer une archive du projet (exclure les fichiers sensibles)
cd /Users/morelsttevensndong/RegO
tar -czf rego.tar.gz \
  --exclude='.venv' \
  --exclude='__pycache__' \
  --exclude='data/*.json' \
  --exclude='exports/*.pdf' \
  --exclude='.env' \
  .
```

### 2. Transférer vers le serveur

```bash
# Remplacez par vos informations serveur
scp rego.tar.gz utilisateur@serveur.com:/chemin/destination/

# Ou avec rsync (plus efficace)
rsync -avz --exclude='.venv' --exclude='__pycache__' \
  /Users/morelsttevensndong/RegO/ \
  utilisateur@serveur.com:/chemin/destination/RegO/
```

### 3. Se connecter au serveur et installer

```bash
# Connexion SSH
ssh utilisateur@serveur.com

# Décompresser (si vous avez utilisé tar)
cd /chemin/destination
tar -xzf rego.tar.gz -C RegO

# Aller dans le dossier
cd RegO

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

```bash
# Créer le fichier .env sur le serveur
cat > .env << 'EOF'
CLIENT_ID=0bf5e2d3-8bd8-4018-bb93-574036e9da92
CLIENT_SECRET=xt_8Q~J7FkfNnN6DBMfmdfZF9egb8BA12quZJa8r
TENANT_ID=79f19744-dc18-4e15-b6b9-a65e89211776
EMAIL_LIMIT=100
DATE_FROM=2024-01-01
EOF

# Sécuriser le fichier
chmod 600 .env
```

### 5. Tester l'application

```bash
# Test simple
python main.py

# Ou en mode non-interactif (script automatisé)
python test_server.py  # (voir ci-dessous pour créer ce script)
```

## 🤖 Méthode 2: Créer un script de test automatisé

Ce script permet de tester RegO sans interaction manuelle:

```python
# test_server.py - À créer sur le serveur
from src.auth import OutlookAuth
from src.email_fetcher import EmailFetcher
from src.registry import EmailRegistry
from src.pdf_exporter import PDFExporter
from config.settings import Config
import sys

def test_rego():
    print("🧪 Test de RegO sur le serveur...\n")
    
    # 1. Test de configuration
    print("1️⃣ Vérification de la configuration...")
    try:
        Config.validate()
        print("   ✅ Configuration valide")
    except Exception as e:
        print(f"   ❌ Erreur de configuration: {e}")
        return False
    
    # 2. Test d'authentification
    print("\n2️⃣ Test d'authentification...")
    try:
        auth = OutlookAuth()
        token = auth.authenticate()
        print("   ✅ Authentification réussie")
    except Exception as e:
        print(f"   ❌ Erreur d'authentification: {e}")
        return False
    
    # 3. Test de récupération des emails
    print("\n3️⃣ Test de récupération des emails...")
    try:
        fetcher = EmailFetcher(token)
        emails = fetcher.fetch_emails(limit=5)
        print(f"   ✅ {len(emails)} emails récupérés")
        
        # Afficher un aperçu
        if emails:
            print(f"   📧 Premier email: {emails[0].get('subject', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Erreur de récupération: {e}")
        return False
    
    # 4. Test du registre
    print("\n4️⃣ Test du système de registre...")
    try:
        registry = EmailRegistry()
        registry.add_emails(emails, overwrite=True)
        stats = registry.get_stats()
        print(f"   ✅ Registre créé: {stats['total']} emails")
    except Exception as e:
        print(f"   ❌ Erreur du registre: {e}")
        return False
    
    # 5. Test d'export PDF
    print("\n5️⃣ Test d'export PDF...")
    try:
        exporter = PDFExporter()
        user_info = fetcher.get_user_info()
        pdf_path = exporter.export_to_pdf(emails, user_info=user_info)
        print(f"   ✅ PDF généré: {pdf_path}")
    except Exception as e:
        print(f"   ❌ Erreur d'export PDF: {e}")
        return False
    
    print("\n" + "="*50)
    print("✅ Tous les tests ont réussi!")
    print("="*50)
    return True

if __name__ == "__main__":
    success = test_rego()
    sys.exit(0 if success else 1)
```

## 🔧 Méthode 3: Créer un service systemd (pour exécution planifiée)

### 1. Créer un script wrapper

```bash
# /chemin/vers/RegO/run_rego.sh
#!/bin/bash

cd /chemin/vers/RegO
source venv/bin/activate

# Récupérer les emails et exporter en PDF
python3 << 'PYTHON_SCRIPT'
from src.auth import OutlookAuth
from src.email_fetcher import EmailFetcher
from src.registry import EmailRegistry
from src.pdf_exporter import PDFExporter
from datetime import datetime

# Authentification
auth = OutlookAuth()
token = auth.authenticate()

# Récupération des emails
fetcher = EmailFetcher(token)
emails = fetcher.fetch_emails(limit=100)

# Sauvegarde dans le registre
registry = EmailRegistry()
registry.add_emails(emails, overwrite=False)

# Export PDF
exporter = PDFExporter()
user_info = fetcher.get_user_info()
pdf_path = exporter.export_to_pdf(
    registry.get_emails(),
    user_info=user_info
)

print(f"✅ {len(emails)} emails traités")
print(f"📄 PDF: {pdf_path}")
PYTHON_SCRIPT
```

### 2. Rendre le script exécutable

```bash
chmod +x /chemin/vers/RegO/run_rego.sh
```

### 3. Tester manuellement

```bash
/chemin/vers/RegO/run_rego.sh
```

### 4. Créer un cron job (optionnel - exécution automatique)

```bash
# Ouvrir crontab
crontab -e

# Ajouter une ligne pour exécuter tous les jours à 8h
0 8 * * * /chemin/vers/RegO/run_rego.sh >> /var/log/rego.log 2>&1
```

## 🐳 Méthode 4: Utiliser Docker (recommandé pour serveur)

### 1. Créer un Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copier les fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variables d'environnement (ou utiliser --env-file)
ENV CLIENT_ID=""
ENV CLIENT_SECRET=""
ENV TENANT_ID=""

CMD ["python", "main.py"]
```

### 2. Créer un docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  rego:
    build: .
    volumes:
      - ./data:/app/data
      - ./exports:/app/exports
    env_file:
      - .env
    stdin_open: true
    tty: true
```

### 3. Construire et lancer

```bash
# Sur le serveur
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Exécuter en mode interactif
docker-compose run rego python main.py
```

## ✅ Tests de validation

### Test rapide d'authentification

```bash
python3 << 'EOF'
from src.auth import OutlookAuth
auth = OutlookAuth()
token = auth.authenticate()
print("✅ Authentification réussie!" if token else "❌ Échec")
EOF
```

### Test de récupération d'emails

```bash
python3 << 'EOF'
from src.auth import OutlookAuth
from src.email_fetcher import EmailFetcher

auth = OutlookAuth()
token = auth.authenticate()
fetcher = EmailFetcher(token)
emails = fetcher.fetch_emails(limit=3)
print(f"✅ {len(emails)} emails récupérés")
for email in emails:
    print(f"  - {email['subject']}")
EOF
```

## 🔒 Sécurité sur serveur

1. **Protéger le fichier .env**
   ```bash
   chmod 600 .env
   chown votre_utilisateur:votre_groupe .env
   ```

2. **Utiliser un utilisateur dédié**
   ```bash
   sudo useradd -m -s /bin/bash rego
   sudo -u rego bash
   ```

3. **Firewall** - Pas de ports à ouvrir (RegO n'est pas un serveur web)

## 📊 Monitoring

### Créer un script de monitoring

```bash
#!/bin/bash
# monitor_rego.sh

LOG_FILE="/var/log/rego_monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

cd /chemin/vers/RegO
source venv/bin/activate

if python test_server.py; then
    echo "[$DATE] ✅ RegO fonctionne correctement" >> $LOG_FILE
else
    echo "[$DATE] ❌ RegO a rencontré une erreur" >> $LOG_FILE
    # Envoyer une alerte (email, slack, etc.)
fi
```

## 🆘 Dépannage serveur

### Problème: Module not found
```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Problème: Permission denied
```bash
# Vérifier les permissions
ls -la .env
chmod 600 .env
```

### Problème: Authentification échoue
```bash
# Vérifier les variables
cat .env
# Tester manuellement
python3 -c "from config.settings import Config; Config.validate()"
```

## 📝 Checklist de déploiement

- [ ] Python 3.8+ installé
- [ ] Fichier .env créé et sécurisé
- [ ] Dépendances installées
- [ ] Test d'authentification réussi
- [ ] Test de récupération d'emails réussi
- [ ] Dossiers data/ et exports/ créés
- [ ] Permissions correctes sur les fichiers
- [ ] (Optionnel) Cron job configuré
- [ ] (Optionnel) Monitoring configuré
