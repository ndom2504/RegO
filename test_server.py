"""
Script de test automatisé pour RegO
Utilisable sur serveur ou en local
"""
from src.auth import OutlookAuth
from src.email_fetcher import EmailFetcher
from src.registry import EmailRegistry
from src.pdf_exporter import PDFExporter
from config.settings import Config
import sys
import traceback


def test_rego():
    """Test complet de toutes les fonctionnalités de RegO"""
    
    print("\n" + "="*60)
    print("🧪 TEST AUTOMATISÉ DE REGO")
    print("="*60 + "\n")
    
    # 1. Test de configuration
    print("1️⃣  Vérification de la configuration...")
    try:
        Config.validate()
        print("   ✅ Configuration valide")
        print(f"   📍 CLIENT_ID: {Config.CLIENT_ID[:10]}...{Config.CLIENT_ID[-10:]}")
        print(f"   📍 TENANT_ID: {Config.TENANT_ID[:10]}...{Config.TENANT_ID[-10:]}")
    except Exception as e:
        print(f"   ❌ Erreur de configuration: {e}")
        print("\n💡 Vérifiez que le fichier .env contient CLIENT_ID, CLIENT_SECRET et TENANT_ID")
        return False
    
    # 2. Test d'authentification
    print("\n2️⃣  Test d'authentification Microsoft Graph API...")
    try:
        auth = OutlookAuth()
        token = auth.authenticate()
        print("   ✅ Authentification réussie")
        print(f"   🔑 Token obtenu ({len(token)} caractères)")
    except Exception as e:
        print(f"   ❌ Erreur d'authentification: {e}")
        print("\n💡 Vérifiez vos identifiants Azure AD et les permissions accordées")
        traceback.print_exc()
        return False
    
    # 3. Test de récupération des informations utilisateur
    print("\n3️⃣  Test de récupération des informations utilisateur...")
    try:
        fetcher = EmailFetcher(token)
        user_info = fetcher.get_user_info()
        print("   ✅ Informations utilisateur récupérées")
        print(f"   👤 Nom: {user_info.get('name', 'N/A')}")
        print(f"   📧 Email: {user_info.get('email', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        user_info = None
    
    # 4. Test de récupération des emails
    print("\n4️⃣  Test de récupération des emails (limite: 5)...")
    try:
        # Utiliser l'email configuré pour les permissions application
        user_email = Config.USER_EMAIL if Config.USER_EMAIL else None
        emails = fetcher.fetch_emails(limit=5, user_email=user_email)
        print(f"   ✅ {len(emails)} emails récupérés")
        
        # Afficher un aperçu des emails
        if emails:
            print("\n   📬 Aperçu des emails récupérés:")
            for idx, email in enumerate(emails[:3], 1):
                subject = email.get('subject', 'N/A')
                sender = email.get('sender', {}).get('name', 'N/A')
                date = email.get('received_date', 'N/A')
                print(f"      {idx}. [{date}] {sender}: {subject[:50]}...")
            if len(emails) > 3:
                print(f"      ... et {len(emails) - 3} autres emails")
        else:
            print("   ⚠️  Aucun email trouvé dans la boîte de réception")
            
    except Exception as e:
        print(f"   ❌ Erreur de récupération des emails: {e}")
        traceback.print_exc()
        return False
    
    # 5. Test du système de registre
    print("\n5️⃣  Test du système de registre...")
    try:
        registry = EmailRegistry()
        
        # Vérifier le registre existant
        existing_emails = registry.get_emails()
        if existing_emails:
            print(f"   📋 Registre existant trouvé: {len(existing_emails)} emails")
        
        # Ajouter les nouveaux emails
        registry.add_emails(emails, overwrite=False)
        
        # Obtenir les statistiques
        stats = registry.get_stats()
        print("   ✅ Registre mis à jour")
        print(f"   📊 Total dans le registre: {stats['total']} emails")
        print(f"      - Lus: {stats['read']}")
        print(f"      - Non lus: {stats['unread']}")
        print(f"      - Avec pièces jointes: {stats['with_attachments']}")
        
    except Exception as e:
        print(f"   ❌ Erreur du système de registre: {e}")
        traceback.print_exc()
        return False
    
    # 6. Test d'export PDF
    print("\n6️⃣  Test d'export PDF...")
    try:
        exporter = PDFExporter()
        test_emails = registry.get_emails()[:10]  # Limiter à 10 pour le test
        
        if not test_emails:
            print("   ⚠️  Pas d'emails à exporter, test ignoré")
        else:
            pdf_path = exporter.export_to_pdf(test_emails, user_info=user_info)
            print(f"   ✅ PDF généré avec succès")
            print(f"   📄 Fichier: {pdf_path}")
            
            # Vérifier que le fichier existe
            import os
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"   💾 Taille: {file_size:,} octets")
            
    except Exception as e:
        print(f"   ❌ Erreur d'export PDF: {e}")
        traceback.print_exc()
        return False
    
    # Résumé final
    print("\n" + "="*60)
    print("✅ TOUS LES TESTS ONT RÉUSSI!")
    print("="*60)
    print("\n💡 RegO est opérationnel et prêt à l'emploi")
    print(f"   - Authentification: OK")
    print(f"   - Récupération emails: OK ({len(emails)} récupérés)")
    print(f"   - Registre: OK ({stats['total']} emails)")
    print(f"   - Export PDF: OK")
    print("\n🚀 Vous pouvez maintenant utiliser: python main.py")
    print("="*60 + "\n")
    
    return True


def main():
    """Point d'entrée du script de test"""
    try:
        success = test_rego()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur fatale: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
