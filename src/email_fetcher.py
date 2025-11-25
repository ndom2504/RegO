"""
Module pour récupérer les emails depuis Outlook via Microsoft Graph API
"""
import requests
from datetime import datetime
from typing import List, Dict
from config.settings import Config


class EmailFetcher:
    """Récupère les emails depuis Outlook"""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        self.graph_endpoint = Config.GRAPH_API_ENDPOINT
    
    def fetch_emails(self, limit: int = None, date_from: str = None, user_email: str = None) -> List[Dict]:
        """
        Récupère les emails de l'utilisateur
        
        Args:
            limit: Nombre maximum d'emails à récupérer
            date_from: Date de début (format: YYYY-MM-DD)
            user_email: Email de l'utilisateur (pour permissions application)
        
        Returns:
            Liste de dictionnaires contenant les détails des emails
        """
        try:
            limit = limit or Config.EMAIL_LIMIT
            
            # Construire l'URL - utiliser /users/{email} pour les permissions application
            if user_email:
                url = f"{self.graph_endpoint}/users/{user_email}/messages"
            else:
                url = f"{self.graph_endpoint}/me/messages"
                
            params = {
                '$top': limit,
                '$orderby': 'receivedDateTime DESC',
                '$select': 'id,subject,from,toRecipients,ccRecipients,receivedDateTime,bodyPreview,hasAttachments,importance,isRead'
            }
            
            # Ajouter un filtre de date si spécifié
            if date_from:
                params['$filter'] = f"receivedDateTime ge {date_from}T00:00:00Z"
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            emails = data.get('value', [])
            
            # Formater les emails
            formatted_emails = [self._format_email(email) for email in emails]
            
            return formatted_emails
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la récupération des emails: {str(e)}")
    
    def _format_email(self, email: Dict) -> Dict:
        """Formate les données de l'email pour le registre"""
        
        # Extraire l'expéditeur
        from_email = email.get('from', {}).get('emailAddress', {})
        sender = {
            'name': from_email.get('name', 'Inconnu'),
            'email': from_email.get('address', '')
        }
        
        # Extraire les destinataires
        to_recipients = []
        for recipient in email.get('toRecipients', []):
            email_addr = recipient.get('emailAddress', {})
            to_recipients.append({
                'name': email_addr.get('name', 'Inconnu'),
                'email': email_addr.get('address', '')
            })
        
        # Extraire les CC
        cc_recipients = []
        for recipient in email.get('ccRecipients', []):
            email_addr = recipient.get('emailAddress', {})
            cc_recipients.append({
                'name': email_addr.get('name', 'Inconnu'),
                'email': email_addr.get('address', '')
            })
        
        # Formater la date
        received_date = email.get('receivedDateTime', '')
        if received_date:
            try:
                dt = datetime.fromisoformat(received_date.replace('Z', '+00:00'))
                formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_date = received_date
        else:
            formatted_date = 'Date inconnue'
        
        return {
            'id': email.get('id', ''),
            'subject': email.get('subject', '(Pas de sujet)'),
            'sender': sender,
            'to': to_recipients,
            'cc': cc_recipients,
            'received_date': formatted_date,
            'preview': email.get('bodyPreview', '')[:200],  # Limiter à 200 caractères
            'has_attachments': email.get('hasAttachments', False),
            'importance': email.get('importance', 'normal'),
            'is_read': email.get('isRead', False)
        }
    
    def get_user_info(self) -> Dict:
        """Récupère les informations de l'utilisateur connecté"""
        try:
            url = f"{self.graph_endpoint}/me"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            user_data = response.json()
            return {
                'name': user_data.get('displayName', 'Inconnu'),
                'email': user_data.get('mail') or user_data.get('userPrincipalName', ''),
                'job_title': user_data.get('jobTitle', ''),
                'office_location': user_data.get('officeLocation', '')
            }
        except requests.exceptions.RequestException as e:
            return {'name': 'Utilisateur', 'email': '', 'job_title': '', 'office_location': ''}
