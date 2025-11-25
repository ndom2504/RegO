"""
Module pour gérer le registre des emails
"""
import json
import os
from datetime import datetime
from typing import List, Dict
from config.settings import Config


class EmailRegistry:
    """Gère le stockage et la récupération des emails dans un registre"""
    
    def __init__(self, registry_file: str = None):
        self.registry_file = registry_file or Config.REGISTRY_FILE
        self.emails = []
        self._load_registry()
    
    def _load_registry(self):
        """Charge le registre depuis le fichier JSON"""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.emails = data.get('emails', [])
            except Exception as e:
                print(f"Erreur lors du chargement du registre: {e}")
                self.emails = []
        else:
            self.emails = []
    
    def save_registry(self):
        """Sauvegarde le registre dans le fichier JSON"""
        try:
            # Créer le dossier si nécessaire
            os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
            
            registry_data = {
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_emails': len(self.emails),
                'emails': self.emails
            }
            
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(registry_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du registre: {e}")
            return False
    
    def add_emails(self, emails: List[Dict], overwrite: bool = False):
        """
        Ajoute des emails au registre
        
        Args:
            emails: Liste d'emails à ajouter
            overwrite: Si True, remplace tous les emails existants
        """
        if overwrite:
            self.emails = emails
        else:
            # Éviter les doublons en vérifiant l'ID
            existing_ids = {email.get('id') for email in self.emails}
            new_emails = [email for email in emails if email.get('id') not in existing_ids]
            self.emails.extend(new_emails)
        
        self.save_registry()
    
    def get_emails(self, filter_func=None) -> List[Dict]:
        """
        Récupère les emails du registre avec un filtre optionnel
        
        Args:
            filter_func: Fonction de filtre à appliquer
        
        Returns:
            Liste d'emails filtrés
        """
        if filter_func:
            return [email for email in self.emails if filter_func(email)]
        return self.emails
    
    def get_stats(self) -> Dict:
        """Retourne des statistiques sur le registre"""
        total = len(self.emails)
        read = sum(1 for email in self.emails if email.get('is_read'))
        unread = total - read
        with_attachments = sum(1 for email in self.emails if email.get('has_attachments'))
        
        # Compter par importance
        importance_counts = {}
        for email in self.emails:
            imp = email.get('importance', 'normal')
            importance_counts[imp] = importance_counts.get(imp, 0) + 1
        
        return {
            'total': total,
            'read': read,
            'unread': unread,
            'with_attachments': with_attachments,
            'importance': importance_counts
        }
    
    def clear_registry(self):
        """Efface tout le registre"""
        self.emails = []
        self.save_registry()
