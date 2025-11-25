"""
Configuration centrale pour RegO
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de l'application RegO"""
    
    # Microsoft Graph API
    CLIENT_ID = os.getenv('CLIENT_ID', '')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET', '')
    TENANT_ID = os.getenv('TENANT_ID', '')
    
    # Scopes nécessaires pour lire les emails
    SCOPES = [
        'https://graph.microsoft.com/.default'
    ]
    
    # Graph API Endpoints
    GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'
    AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
    
    # Paramètres des emails
    EMAIL_LIMIT = int(os.getenv('EMAIL_LIMIT', 100))
    DATE_FROM = os.getenv('DATE_FROM', '2024-01-01')
    USER_EMAIL = os.getenv('USER_EMAIL', '')
    
    # Chemins des dossiers
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    EXPORTS_DIR = os.path.join(BASE_DIR, 'exports')
    CONFIG_DIR = os.path.join(BASE_DIR, 'config')
    
    # Nom du fichier de registre
    REGISTRY_FILE = os.path.join(DATA_DIR, 'email_registry.json')
    
    @staticmethod
    def validate():
        """Valide la configuration"""
        if not Config.CLIENT_ID:
            raise ValueError("CLIENT_ID manquant dans .env")
        if not Config.CLIENT_SECRET:
            raise ValueError("CLIENT_SECRET manquant dans .env")
        if not Config.TENANT_ID:
            raise ValueError("TENANT_ID manquant dans .env")
        return True
