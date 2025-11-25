"""
Interface en ligne de commande pour RegO
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich import box
import sys

from src.auth import OutlookAuth
from src.email_fetcher import EmailFetcher
from src.registry import EmailRegistry
from src.pdf_exporter import PDFExporter
from config.settings import Config


class RegOCLI:
    """Interface en ligne de commande pour RegO"""
    
    def __init__(self):
        self.console = Console()
        self.registry = EmailRegistry()
        self.access_token = None
        self.user_info = None
    
    def show_banner(self):
        """Affiche la bannière de l'application"""
        banner = """
        ╔═══════════════════════════════════════════╗
        ║                                           ║
        ║        📧 RegO - Registre Outlook 📧      ║
        ║                                           ║
        ║    Gestion de vos courriels Outlook      ║
        ║         en registre exportable           ║
        ║                                           ║
        ╚═══════════════════════════════════════════╝
        """
        self.console.print(banner, style="bold blue")
    
    def authenticate(self):
        """Authentifie l'utilisateur avec Outlook"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("[cyan]Authentification en cours...", total=None)
                
                auth = OutlookAuth()
                self.access_token = auth.authenticate()
                
                progress.update(task, completed=True)
            
            self.console.print("✅ Authentification réussie!", style="bold green")
            
            # Récupérer les infos utilisateur
            fetcher = EmailFetcher(self.access_token)
            self.user_info = fetcher.get_user_info()
            
            if self.user_info.get('name'):
                self.console.print(f"👤 Connecté en tant que: {self.user_info['name']}", style="cyan")
            
            return True
            
        except Exception as e:
            self.console.print(f"❌ Erreur d'authentification: {str(e)}", style="bold red")
            return False
    
    def fetch_and_store_emails(self):
        """Récupère et stocke les emails"""
        if not self.access_token:
            self.console.print("⚠️  Vous devez d'abord vous authentifier.", style="yellow")
            return
        
        try:
            # Demander le nombre d'emails
            limit_input = Prompt.ask(
                "Combien d'emails voulez-vous récupérer?",
                default=str(Config.EMAIL_LIMIT)
            )
            limit = int(limit_input)
            
            # Demander si on veut écraser le registre existant
            overwrite = False
            if self.registry.get_emails():
                overwrite = Confirm.ask(
                    f"Le registre contient déjà {len(self.registry.get_emails())} emails. Voulez-vous les remplacer?",
                    default=False
                )
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task(f"[cyan]Récupération de {limit} emails...", total=None)
                
                fetcher = EmailFetcher(self.access_token)
                # Utiliser l'email utilisateur si configuré (pour permissions application)
                emails = fetcher.fetch_emails(limit=limit, user_email=Config.USER_EMAIL or None)
                
                progress.update(task, completed=True)
            
            # Stocker dans le registre
            self.registry.add_emails(emails, overwrite=overwrite)
            
            self.console.print(f"✅ {len(emails)} emails récupérés et stockés!", style="bold green")
            
        except ValueError:
            self.console.print("❌ Veuillez entrer un nombre valide.", style="bold red")
        except Exception as e:
            self.console.print(f"❌ Erreur: {str(e)}", style="bold red")
    
    def show_registry_stats(self):
        """Affiche les statistiques du registre"""
        emails = self.registry.get_emails()
        
        if not emails:
            self.console.print("📭 Le registre est vide.", style="yellow")
            return
        
        stats = self.registry.get_stats()
        
        # Créer un tableau de statistiques
        table = Table(title="📊 Statistiques du Registre", box=box.ROUNDED)
        table.add_column("Statistique", style="cyan", no_wrap=True)
        table.add_column("Valeur", style="magenta")
        
        table.add_row("Total d'emails", str(stats['total']))
        table.add_row("Emails lus", str(stats['read']))
        table.add_row("Emails non lus", str(stats['unread']))
        table.add_row("Avec pièces jointes", str(stats['with_attachments']))
        
        # Importance
        for imp, count in stats['importance'].items():
            imp_label = {'high': 'Importants', 'normal': 'Normaux', 'low': 'Faible priorité'}.get(imp, imp)
            table.add_row(imp_label, str(count))
        
        self.console.print(table)
    
    def show_email_list(self):
        """Affiche la liste des emails"""
        emails = self.registry.get_emails()
        
        if not emails:
            self.console.print("📭 Le registre est vide.", style="yellow")
            return
        
        # Limiter l'affichage aux 20 premiers emails
        display_limit = 20
        emails_to_show = emails[:display_limit]
        
        table = Table(title=f"📧 Liste des Emails (affichage de {len(emails_to_show)}/{len(emails)})", box=box.ROUNDED)
        table.add_column("#", style="cyan", width=4)
        table.add_column("Date", style="green", width=17)
        table.add_column("De", style="blue", width=25)
        table.add_column("Sujet", style="yellow", width=40)
        table.add_column("Statut", style="magenta", width=15)
        
        for idx, email in enumerate(emails_to_show, 1):
            sender = email.get('sender', {})
            sender_name = sender.get('name', 'Inconnu')
            
            subject = email.get('subject', '(Pas de sujet)')
            if len(subject) > 40:
                subject = subject[:37] + '...'
            
            status = '✉️ Non lu' if not email.get('is_read') else '✓ Lu'
            if email.get('has_attachments'):
                status += ' 📎'
            if email.get('importance') == 'high':
                status += ' ⚠️'
            
            table.add_row(
                str(idx),
                email.get('received_date', '')[:16],
                sender_name[:25],
                subject,
                status
            )
        
        self.console.print(table)
        
        if len(emails) > display_limit:
            self.console.print(f"\n💡 {len(emails) - display_limit} autres emails non affichés.", style="dim")
    
    def export_to_pdf(self):
        """Exporte le registre en PDF"""
        emails = self.registry.get_emails()
        
        if not emails:
            self.console.print("📭 Le registre est vide. Rien à exporter.", style="yellow")
            return
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("[cyan]Génération du PDF...", total=None)
                
                exporter = PDFExporter()
                pdf_path = exporter.export_to_pdf(emails, user_info=self.user_info)
                
                progress.update(task, completed=True)
            
            self.console.print(f"✅ PDF généré avec succès!", style="bold green")
            self.console.print(f"📄 Fichier: {pdf_path}", style="cyan")
            
        except Exception as e:
            self.console.print(f"❌ Erreur lors de l'export PDF: {str(e)}", style="bold red")
    
    def show_menu(self):
        """Affiche le menu principal"""
        menu_items = [
            "1. 🔐 S'authentifier avec Outlook",
            "2. 📥 Récupérer les emails",
            "3. 📊 Voir les statistiques",
            "4. 📋 Voir la liste des emails",
            "5. 📄 Exporter en PDF",
            "6. 🗑️  Effacer le registre",
            "7. ❌ Quitter"
        ]
        
        self.console.print("\n" + "="*50, style="bold")
        self.console.print("MENU PRINCIPAL", style="bold cyan", justify="center")
        self.console.print("="*50 + "\n", style="bold")
        
        for item in menu_items:
            self.console.print(f"  {item}")
        
        self.console.print()
    
    def clear_registry(self):
        """Efface le registre"""
        if not self.registry.get_emails():
            self.console.print("📭 Le registre est déjà vide.", style="yellow")
            return
        
        if Confirm.ask("⚠️  Êtes-vous sûr de vouloir effacer tous les emails du registre?", default=False):
            self.registry.clear_registry()
            self.console.print("✅ Registre effacé avec succès!", style="bold green")
    
    def run(self):
        """Lance l'application"""
        self.show_banner()
        
        # Vérifier la configuration
        try:
            Config.validate()
        except ValueError as e:
            self.console.print(f"❌ Erreur de configuration: {str(e)}", style="bold red")
            self.console.print("💡 Veuillez configurer le fichier .env avec vos identifiants Azure.", style="yellow")
            return
        
        while True:
            self.show_menu()
            choice = Prompt.ask("Choisissez une option", choices=["1", "2", "3", "4", "5", "6", "7"])
            
            if choice == "1":
                self.authenticate()
            elif choice == "2":
                self.fetch_and_store_emails()
            elif choice == "3":
                self.show_registry_stats()
            elif choice == "4":
                self.show_email_list()
            elif choice == "5":
                self.export_to_pdf()
            elif choice == "6":
                self.clear_registry()
            elif choice == "7":
                self.console.print("\n👋 Au revoir!", style="bold blue")
                break


def main():
    """Point d'entrée principal"""
    try:
        cli = RegOCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir!")
        sys.exit(0)
    except Exception as e:
        console = Console()
        console.print(f"\n❌ Erreur fatale: {str(e)}", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main()
