"""
Modèles de base de données pour RegO
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
import json
import hashlib

db = SQLAlchemy()


def hash_password(password):
    """Hash le mot de passe avec SHA256 (compatible tous systèmes)"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, password_hash):
    """Vérifie le mot de passe"""
    return hash_password(password) == password_hash


class User(UserMixin, db.Model):
    """Modèle utilisateur pour l'authentification multi-utilisateurs"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    company = db.Column(db.String(120))
    
    # Configuration Outlook spécifique à l'utilisateur
    outlook_email = db.Column(db.String(120))
    client_id = db.Column(db.String(255))
    client_secret = db.Column(db.String(255))
    tenant_id = db.Column(db.String(255))
    
    # OAuth2 tokens (pour connexion automatique Microsoft)
    microsoft_access_token = db.Column(db.Text)
    microsoft_refresh_token = db.Column(db.Text)
    microsoft_token_expiry = db.Column(db.DateTime)
    microsoft_user_id = db.Column(db.String(255))  # ID Microsoft unique
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relations
    communications = db.relationship('Communication', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash le mot de passe"""
        self.password_hash = hash_password(password)
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return verify_password(password, self.password_hash)
    
    def has_outlook_config(self):
        """Vérifie si l'utilisateur a configuré Outlook"""
        return all([self.outlook_email, self.client_id, self.client_secret, self.tenant_id])
    
    def has_microsoft_oauth(self):
        """Vérifie si l'utilisateur est connecté via OAuth Microsoft"""
        if not self.microsoft_access_token:
            return False
        # Vérifier si le token n'est pas expiré
        if self.microsoft_token_expiry and self.microsoft_token_expiry > datetime.utcnow():
            return True
        return False
    
    def set_microsoft_tokens(self, access_token, refresh_token=None, expires_in=3600):
        """Enregistre les tokens OAuth Microsoft"""
        self.microsoft_access_token = access_token
        if refresh_token:
            self.microsoft_refresh_token = refresh_token
        self.microsoft_token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'company': self.company,
            'outlook_email': self.outlook_email,
            'has_outlook_config': self.has_outlook_config(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_admin': self.is_admin
        }


class Communication(db.Model):
    """Modèle pour le registre des communications"""
    __tablename__ = 'communications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Identifiant unique de l'email (depuis Outlook)
    email_id = db.Column(db.String(255), unique=True)
    
    # Informations de l'email
    subject = db.Column(db.Text)
    sender_name = db.Column(db.String(255))
    sender_email = db.Column(db.String(255))
    recipients = db.Column(db.Text)  # JSON string
    cc_recipients = db.Column(db.Text)  # JSON string
    
    received_date = db.Column(db.DateTime)
    body_preview = db.Column(db.Text)
    
    # Métadonnées
    has_attachments = db.Column(db.Boolean, default=False)
    is_read = db.Column(db.Boolean, default=False)
    importance = db.Column(db.String(20))
    
    # Catégories et tags personnalisés
    category = db.Column(db.String(50))
    tags = db.Column(db.Text)  # JSON string
    notes = db.Column(db.Text)
    
    # Traçabilité
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_recipients(self, recipients_list):
        """Convertit la liste des destinataires en JSON"""
        self.recipients = json.dumps(recipients_list)
    
    def get_recipients(self):
        """Récupère la liste des destinataires"""
        if self.recipients:
            return json.loads(self.recipients)
        return []
    
    def set_cc_recipients(self, cc_list):
        """Convertit la liste des CC en JSON"""
        self.cc_recipients = json.dumps(cc_list)
    
    def get_cc_recipients(self):
        """Récupère la liste des CC"""
        if self.cc_recipients:
            return json.loads(self.cc_recipients)
        return []
    
    def set_tags(self, tags_list):
        """Convertit la liste des tags en JSON"""
        self.tags = json.dumps(tags_list)
    
    def get_tags(self):
        """Récupère la liste des tags"""
        if self.tags:
            return json.loads(self.tags)
        return []
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'email_id': self.email_id,
            'subject': self.subject,
            'sender': {
                'name': self.sender_name,
                'email': self.sender_email
            },
            'recipients': self.get_recipients(),
            'cc': self.get_cc_recipients(),
            'received_date': self.received_date.strftime('%Y-%m-%d %H:%M:%S') if self.received_date else None,
            'body_preview': self.body_preview,
            'has_attachments': self.has_attachments,
            'is_read': self.is_read,
            'importance': self.importance,
            'category': self.category,
            'tags': self.get_tags(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
