# Utiliser Python 3.9 slim pour une image légère
FROM python:3.9-slim

# Variables d'environnement pour Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Créer le répertoire de travail
WORKDIR /app

# Copier les dépendances d'abord (pour cache Docker)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copier tout le code de l'application
COPY . .

# Créer le dossier pour les PDFs
RUN mkdir -p emails_pdf && chmod 777 emails_pdf

# Créer la base de données si elle n'existe pas
RUN python migrate_db.py || true

# Exposer le port (Cloud Run utilise $PORT)
EXPOSE 8080

# Commande de démarrage avec Gunicorn
CMD exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 0 app_pro:app
