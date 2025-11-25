"""
Module d'authentification Microsoft Graph API
"""
import msal
from config.settings import Config


class OutlookAuth:
    """Gère l'authentification avec Microsoft Graph API"""
    
    def __init__(self):
        self.client_id = Config.CLIENT_ID
        self.client_secret = Config.CLIENT_SECRET
        self.authority = Config.AUTHORITY
        self.scopes = Config.SCOPES
        self.app = None
        self.access_token = None
    
    def authenticate(self):
        """
        Authentifie l'application avec Microsoft Graph API
        Retourne un token d'accès
        """
        try:
            # Créer une application confidentielle MSAL
            self.app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=self.authority,
                client_credential=self.client_secret
            )
            
            # Acquérir un token
            result = self.app.acquire_token_for_client(scopes=self.scopes)
            
            if "access_token" in result:
                self.access_token = result['access_token']
                return self.access_token
            else:
                error_msg = result.get('error_description', 'Erreur d\'authentification')
                raise Exception(f"Échec de l'authentification: {error_msg}")
                
        except Exception as e:
            raise Exception(f"Erreur lors de l'authentification: {str(e)}")
    
    def get_token(self):
        """Retourne le token d'accès actuel ou en obtient un nouveau"""
        if not self.access_token:
            return self.authenticate()
        return self.access_token
