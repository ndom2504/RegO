"""
Script pour migrer la base de données et ajouter les nouveaux champs OAuth
"""
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_pro import app, db
from src.models import User, Communication

print("🔄 Migration de la base de données...")

with app.app_context():
    # Option 1: Ajouter les colonnes manquantes (si la DB existe)
    try:
        from sqlalchemy import text
        
        # Vérifier si les colonnes existent déjà
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        new_columns = {
            'microsoft_access_token': 'TEXT',
            'microsoft_refresh_token': 'TEXT',
            'microsoft_token_expiry': 'DATETIME',
            'microsoft_user_id': 'VARCHAR(255)'
        }
        
        for col_name, col_type in new_columns.items():
            if col_name not in columns:
                print(f"➕ Ajout de la colonne {col_name}...")
                db.session.execute(text(f'ALTER TABLE users ADD COLUMN {col_name} {col_type}'))
        
        db.session.commit()
        print("✅ Migration réussie!")
        
    except Exception as e:
        print(f"⚠️  Erreur lors de la migration: {e}")
        print("🔄 Recréation de la base de données...")
        
        # Option 2: Recréer toutes les tables
        db.drop_all()
        db.create_all()
        
        # Recréer l'admin par défaut
        admin = User(
            username='admin',
            email='admin@rego.local',
            full_name='Administrateur',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Base de données recréée avec succès!")
        print("👤 Compte admin: admin / admin123")

print("\n🎉 Migration terminée!")
