"""
Application web Flask pour RegO avec dashboard
"""
from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import os
from datetime import datetime

from src.auth import OutlookAuth
from src.email_fetcher import EmailFetcher
from src.registry import EmailRegistry
from src.pdf_exporter import PDFExporter
from config.settings import Config

app = Flask(__name__)
CORS(app)

# Variables globales pour stocker l'état
auth_token = None
registry = EmailRegistry()


@app.route('/')
def dashboard():
    """Page principale du dashboard"""
    return render_template('dashboard.html')


@app.route('/api/status')
def status():
    """Retourne l'état de l'application"""
    global auth_token
    
    stats = registry.get_stats() if registry.get_emails() else {
        'total': 0, 'read': 0, 'unread': 0, 'with_attachments': 0, 'importance': {}
    }
    
    return jsonify({
        'authenticated': auth_token is not None,
        'user_email': Config.USER_EMAIL,
        'stats': stats
    })


@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """Authentifie avec Microsoft Graph API"""
    global auth_token
    
    try:
        auth = OutlookAuth()
        auth_token = auth.authenticate()
        
        return jsonify({
            'success': True,
            'message': 'Authentification réussie!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/fetch-emails', methods=['POST'])
def fetch_emails():
    """Récupère les emails depuis Outlook"""
    global auth_token
    
    if not auth_token:
        return jsonify({
            'success': False,
            'error': 'Vous devez d\'abord vous authentifier'
        }), 401
    
    try:
        data = request.json
        limit = data.get('limit', Config.EMAIL_LIMIT)
        overwrite = data.get('overwrite', False)
        
        fetcher = EmailFetcher(auth_token)
        emails = fetcher.fetch_emails(limit=limit, user_email=Config.USER_EMAIL)
        
        registry.add_emails(emails, overwrite=overwrite)
        
        return jsonify({
            'success': True,
            'message': f'{len(emails)} emails récupérés',
            'count': len(emails)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/emails')
def get_emails():
    """Retourne la liste des emails"""
    try:
        emails = registry.get_emails()
        return jsonify({
            'success': True,
            'emails': emails,
            'count': len(emails)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/export-pdf', methods=['POST'])
def export_pdf():
    """Génère et retourne un PDF"""
    global auth_token
    
    try:
        emails = registry.get_emails()
        
        if not emails:
            return jsonify({
                'success': False,
                'error': 'Aucun email dans le registre'
            }), 400
        
        # Récupérer les infos utilisateur si authentifié
        user_info = None
        if auth_token:
            try:
                fetcher = EmailFetcher(auth_token)
                user_info = fetcher.get_user_info()
            except:
                pass
        
        exporter = PDFExporter()
        pdf_path = exporter.export_to_pdf(emails, user_info=user_info)
        
        return jsonify({
            'success': True,
            'message': 'PDF généré avec succès',
            'filename': os.path.basename(pdf_path),
            'path': pdf_path
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/download-pdf/<filename>')
def download_pdf(filename):
    """Télécharge un fichier PDF"""
    try:
        pdf_path = os.path.join(Config.EXPORTS_DIR, filename)
        
        if not os.path.exists(pdf_path):
            return jsonify({
                'success': False,
                'error': 'Fichier non trouvé'
            }), 404
        
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/clear-registry', methods=['POST'])
def clear_registry():
    """Efface le registre"""
    try:
        registry.clear_registry()
        return jsonify({
            'success': True,
            'message': 'Registre effacé avec succès'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/stats')
def get_stats():
    """Retourne les statistiques détaillées"""
    try:
        stats = registry.get_stats()
        emails = registry.get_emails()
        
        # Statistiques par expéditeur
        senders = {}
        for email in emails:
            sender_name = email.get('sender', {}).get('name', 'Inconnu')
            senders[sender_name] = senders.get(sender_name, 0) + 1
        
        # Top 5 expéditeurs
        top_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Emails par jour (derniers 7 jours)
        emails_by_day = {}
        for email in emails:
            date_str = email.get('received_date', '')[:10]  # YYYY-MM-DD
            if date_str:
                emails_by_day[date_str] = emails_by_day.get(date_str, 0) + 1
        
        return jsonify({
            'success': True,
            'stats': stats,
            'top_senders': [{'name': name, 'count': count} for name, count in top_senders],
            'emails_by_day': emails_by_day
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


if __name__ == '__main__':
    # Vérifier la configuration
    try:
        Config.validate()
        print("\n" + "="*60)
        print("🚀 Lancement du dashboard RegO")
        print("="*60)
        print(f"📧 Email configuré: {Config.USER_EMAIL}")
        print(f"🌐 Dashboard accessible sur: http://localhost:5000")
        print("="*60 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        print("💡 Vérifiez votre fichier .env")
