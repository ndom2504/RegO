"""
Script d'initialisation de la base de données pour Render
"""
from app_pro import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Base de données initialisée avec succès!")
