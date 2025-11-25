"""
Gestionnaire OAuth2 pour Microsoft (Azure AD)
Permet aux utilisateurs de se connecter avec leur compte Microsoft
"""
import os
from authlib.integrations.flask_client import OAuth
from flask import url_for


class MicrosoftOAuth:
    """Gestionnaire OAuth2 pour Microsoft"""
    
    # Configuration centralisée - à configurer via variables d'environnement
    # Ces identifiants sont pour VOTRE application Azure AD partagée
    CLIENT_ID = os.getenv('MICROSOFT_CLIENT_ID', '')
    CLIENT_SECRET = os.getenv('MICROSOFT_CLIENT_SECRET', '')
    TENANT_ID = os.getenv('MICROSOFT_TENANT_ID', 'common')  # 'common' pour multi-tenant
    
    # Scopes nécessaires pour lire les emails
    SCOPES = [
        'openid',
        'profile',
        'email',
        'User.Read',
        'Mail.Read',
        'Mail.ReadBasic'
    ]
    
    # URLs Microsoft
    AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
    AUTHORIZE_URL = f'{AUTHORITY}/oauth2/v2.0/authorize'
    TOKEN_URL = f'{AUTHORITY}/oauth2/v2.0/token'
    
    def __init__(self, app=None):
        """Initialise OAuth avec Flask"""
        self.oauth = OAuth()
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Configure OAuth avec l'application Flask"""
        self.oauth.init_app(app)
        
        # Enregistrer le client Microsoft
        self.oauth.register(
            name='microsoft',
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            server_metadata_url=f'{self.AUTHORITY}/v2.0/.well-known/openid-configuration',
            client_kwargs={
                'scope': ' '.join(self.SCOPES),
                'code_challenge_method': 'S256'  # Active PKCE (requis par Azure AD)
            }
        )
    
    def get_authorize_url(self, redirect_uri):
        """Génère l'URL d'autorisation Microsoft"""
        return self.oauth.microsoft.authorize_redirect(redirect_uri)
    
    def get_token(self, redirect_uri):
        """Récupère le token après autorisation"""
        # Authlib requiert le même redirect_uri que celui utilisé à l'étape d'authorize
        # et gère automatiquement le PKCE via la session
        token = self.oauth.microsoft.authorize_access_token(redirect_uri=redirect_uri)
        return token
    
    def get_user_info(self, token):
        """Récupère les informations de l'utilisateur"""
        resp = self.oauth.microsoft.get('https://graph.microsoft.com/v1.0/me', token=token)
        return resp.json()
    
    @staticmethod
    def get_user_emails_with_token(access_token, user_email=None, limit=50):
        """
        Récupère les emails en utilisant le token OAuth
        Compatible avec EmailFetcher existant
        """
        from src.email_fetcher import EmailFetcher
        
        fetcher = EmailFetcher(access_token)
        return fetcher.fetch_emails(limit=limit, user_email=user_email)
