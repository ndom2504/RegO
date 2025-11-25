"""
Application web Flask professionnelle pour RegO
Version commerciale avec authentification multi-utilisateurs
"""
from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, session, flash
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import os
from datetime import datetime, timedelta

from src.models import db, User, Communication
from src.auth import OutlookAuth
from src.email_fetcher import EmailFetcher
from src.pdf_exporter import PDFExporter
from src.microsoft_oauth import MicrosoftOAuth
from config.settings import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rego.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

CORS(app)
db.init_app(app)

# Configuration OAuth Microsoft
microsoft_oauth = MicrosoftOAuth(app)

# Configuration Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================== ROUTES D'AUTHENTIFICATION ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember', False)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=remember)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        
        return jsonify({'success': False, 'error': 'Identifiants invalides'}), 401
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Page d'inscription"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.json
        
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'error': 'Ce nom d\'utilisateur existe déjà'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Cet email est déjà utilisé'}), 400
        
        # Créer le nouvel utilisateur
        user = User(
            username=data['username'],
            email=data['email'],
            full_name=data.get('full_name', ''),
            company=data.get('company', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Compte créé avec succès', 'redirect': url_for('login')})
    
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    """Déconnexion"""
    logout_user()
    return redirect(url_for('login'))


# ==================== ROUTES OAUTH MICROSOFT ====================

@app.route('/auth/microsoft')
def auth_microsoft():
    """Redirige vers la page de connexion Microsoft"""
    redirect_uri = url_for('auth_microsoft_callback', _external=True)
    return microsoft_oauth.get_authorize_url(redirect_uri)


@app.route('/auth/microsoft/callback')
def auth_microsoft_callback():
    """Callback après authentification Microsoft"""
    try:
        # Récupérer le token
        redirect_uri = url_for('auth_microsoft_callback', _external=True)
        token = microsoft_oauth.get_token(redirect_uri)
        
        # Récupérer les infos utilisateur
        user_info = microsoft_oauth.get_user_info(token)
        
        microsoft_id = user_info.get('id')
        email = user_info.get('mail') or user_info.get('userPrincipalName')
        display_name = user_info.get('displayName', '')
        
        # Chercher l'utilisateur existant par microsoft_id ou email
        user = User.query.filter_by(microsoft_user_id=microsoft_id).first()
        
        if not user:
            # Chercher par email
            user = User.query.filter_by(email=email).first()
            
            if not user:
                # Créer un nouvel utilisateur
                username = email.split('@')[0]
                
                # S'assurer que le username est unique
                base_username = username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User(
                    username=username,
                    email=email,
                    full_name=display_name,
                    outlook_email=email,
                    microsoft_user_id=microsoft_id
                )
                # Générer un mot de passe aléatoire (non utilisé pour OAuth)
                import secrets
                user.set_password(secrets.token_urlsafe(32))
                
                db.session.add(user)
        
        # Mettre à jour les tokens OAuth
        access_token = token.get('access_token')
        refresh_token = token.get('refresh_token')
        expires_in = token.get('expires_in', 3600)
        
        user.set_microsoft_tokens(access_token, refresh_token, expires_in)
        user.microsoft_user_id = microsoft_id
        user.outlook_email = email
        user.last_login = datetime.utcnow()
        
        db.session.commit()
        
        # Connecter l'utilisateur
        login_user(user, remember=True)
        
        flash(f'Connexion réussie! Bienvenue {display_name}', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        flash(f'Erreur d\'authentification Microsoft: {str(e)}', 'error')
        return redirect(url_for('login'))


# ==================== ROUTES DU DASHBOARD ====================

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    return render_template('dashboard_pro.html', user=current_user)


@app.route('/communications')
@login_required
def communications():
    """Page du registre des communications"""
    return render_template('communications.html', user=current_user)


@app.route('/profile')
@login_required
def profile():
    """Page de profil utilisateur"""
    return render_template('profile.html', user=current_user)


# ==================== API ENDPOINTS ====================

@app.route('/api/user')
@app.route('/api/user/info')
@login_required
def user_info():
    """Retourne les informations de l'utilisateur connecté"""
    user_dict = current_user.to_dict()
    # Ajouter les champs manquants pour compatibilité
    user_dict['outlook_client_id'] = current_user.client_id
    user_dict['outlook_tenant_id'] = current_user.tenant_id
    user_dict['outlook_client_secret'] = current_user.client_secret if current_user.client_secret else None
    return jsonify({
        'success': True,
        'user': user_dict
    })


@app.route('/api/user/update', methods=['POST'])
@login_required
def update_user():
    """Met à jour les informations utilisateur"""
    data = request.json
    
    if 'email' in data:
        # Vérifier si l'email n'est pas déjà utilisé par un autre utilisateur
        existing = User.query.filter(User.email == data['email'], User.id != current_user.id).first()
        if existing:
            return jsonify({'success': False, 'error': 'Cet email est déjà utilisé'}), 400
        current_user.email = data['email']
    
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    
    if 'company' in data:
        current_user.company = data['company']
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Profil mis à jour avec succès'})


@app.route('/api/user/change-password', methods=['POST'])
@login_required
def change_password():
    """Change le mot de passe utilisateur"""
    data = request.json
    new_password = data.get('new_password')
    
    if not new_password or len(new_password) < 6:
        return jsonify({'success': False, 'error': 'Le mot de passe doit contenir au moins 6 caractères'}), 400
    
    current_user.set_password(new_password)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Mot de passe modifié avec succès'})


@app.route('/api/outlook/configure', methods=['POST'])
@login_required
def configure_outlook():
    """Configure les paramètres Outlook de l'utilisateur"""
    data = request.json
    
    current_user.client_id = data.get('outlook_client_id')
    current_user.client_secret = data.get('outlook_client_secret')
    current_user.tenant_id = data.get('outlook_tenant_id')
    current_user.outlook_email = data.get('outlook_email')
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Configuration Outlook enregistrée'})


@app.route('/api/outlook/test', methods=['GET'])
@login_required
def test_outlook():
    """Teste la connexion Outlook"""
    if not current_user.has_outlook_config():
        return jsonify({'success': False, 'error': 'Configuration Outlook manquante'}), 400
    
    try:
        auth = OutlookAuth()
        auth.client_id = current_user.client_id
        auth.client_secret = current_user.client_secret
        auth.authority = f'https://login.microsoftonline.com/{current_user.tenant_id}'
        
        token = auth.authenticate()
        
        # Tester en récupérant 1 email
        fetcher = EmailFetcher(token)
        emails = fetcher.fetch_emails(limit=1, user_email=current_user.outlook_email)
        
        return jsonify({
            'success': True,
            'message': f'Connexion réussie! {len(emails)} email(s) trouvé(s)'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/sync', methods=['POST'])
@login_required
def sync_emails():
    """Synchronise les emails Outlook avec la base de données"""
    # Vérifier si l'utilisateur a une connexion OAuth valide
    if current_user.has_microsoft_oauth():
        # Utiliser le token OAuth
        token = current_user.microsoft_access_token
        try:
            fetcher = EmailFetcher(token)
            emails = fetcher.fetch_emails(limit=50, user_email=current_user.outlook_email)
            
            # Enregistrer dans la base de données
            new_count = 0
            
            for email_data in emails:
                # Vérifier si existe déjà
                existing = Communication.query.filter_by(
                    email_id=email_data['id'],
                    user_id=current_user.id
                ).first()
                
                if not existing:
                    comm = Communication(
                        user_id=current_user.id,
                        email_id=email_data['id'],
                        subject=email_data.get('subject', ''),
                        sender_name=email_data.get('sender', {}).get('name', ''),
                        sender_email=email_data.get('sender', {}).get('email', '')
                    )
                    
                    # Parser la date
                    date_str = email_data.get('received_date', '')
                    try:
                        comm.received_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    except:
                        comm.received_date = datetime.utcnow()
                    
                    comm.body_preview = email_data.get('preview', '')
                    comm.has_attachments = email_data.get('has_attachments', False)
                    comm.importance = email_data.get('importance', 'normal')
                    
                    db.session.add(comm)
                    new_count += 1
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'count': new_count,
                'message': f'{new_count} nouveaux emails synchronisés',
                'method': 'oauth'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': f'OAuth: {str(e)}'}), 400
    
    # Sinon utiliser l'ancienne méthode avec config manuelle
    if not current_user.has_outlook_config():
        return jsonify({
            'success': False,
            'error': 'Veuillez vous connecter avec Microsoft ou configurer vos identifiants Outlook manuellement'
        }), 400
    
    try:
        # Authentifier
        auth = OutlookAuth()
        auth.client_id = current_user.client_id
        auth.client_secret = current_user.client_secret
        auth.authority = f'https://login.microsoftonline.com/{current_user.tenant_id}'
        
        token = auth.authenticate()
        
        # Récupérer les emails
        fetcher = EmailFetcher(token)
        emails = fetcher.fetch_emails(limit=50, user_email=current_user.outlook_email)
        
        # Enregistrer dans la base de données
        new_count = 0
        
        for email_data in emails:
            # Vérifier si existe déjà
            existing = Communication.query.filter_by(
                email_id=email_data['id'],
                user_id=current_user.id
            ).first()
            
            if not existing:
                comm = Communication(
                    user_id=current_user.id,
                    email_id=email_data['id'],
                    subject=email_data.get('subject', ''),
                    sender_name=email_data.get('sender', {}).get('name', ''),
                    sender_email=email_data.get('sender', {}).get('email', '')
                )
                
                # Parser la date
                date_str = email_data.get('received_date', '')
                try:
                    comm.received_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                except:
                    comm.received_date = datetime.utcnow()
                
                comm.body_preview = email_data.get('preview', '')
                comm.has_attachments = email_data.get('has_attachments', False)
                comm.importance = email_data.get('importance', 'normal')
                
                db.session.add(comm)
                new_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'count': new_count,
            'message': f'{new_count} nouveaux emails synchronisés'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/communications/stats', methods=['GET'])
@login_required
def communications_stats():
    """Retourne les statistiques des communications"""
    from sqlalchemy import func, extract
    
    total = Communication.query.filter_by(user_id=current_user.id).count()
    
    # Communications du mois en cours
    now = datetime.utcnow()
    this_month = Communication.query.filter(
        Communication.user_id == current_user.id,
        extract('year', Communication.received_date) == now.year,
        extract('month', Communication.received_date) == now.month
    ).count()
    
    # Nombre de catégories uniques
    categories = db.session.query(func.count(func.distinct(Communication.category))).filter(
        Communication.user_id == current_user.id,
        Communication.category.isnot(None)
    ).scalar()
    
    return jsonify({
        'success': True,
        'total': total,
        'this_month': this_month,
        'categories': categories or 0
    })


@app.route('/api/communications/list', methods=['GET'])
@login_required
def communications_list():
    """Retourne la liste des communications"""
    limit = request.args.get('limit', type=int)
    
    query = Communication.query.filter_by(user_id=current_user.id).order_by(Communication.received_date.desc())
    
    if limit:
        query = query.limit(limit)
    
    communications = query.all()
    
    return jsonify({
        'success': True,
        'communications': [{
            'id': c.id,
            'subject': c.subject,
            'sender': c.sender_name or c.sender_email,
            'received_date': c.received_date.isoformat() if c.received_date else None,
            'category': c.category,
            'tags': c.get_tags(),
            'recipients': c.get_recipients(),
            'notes': c.notes
        } for c in communications]
    })


@app.route('/api/export-pdf', methods=['GET'])
@login_required
def export_pdf():
    """Exporte le registre des communications en PDF"""
    try:
        # Récupérer toutes les communications de l'utilisateur
        communications = Communication.query.filter_by(user_id=current_user.id).order_by(Communication.received_date.desc()).all()
        
        # Convertir en format attendu par PDFExporter
        emails_data = [{
            'subject': c.subject,
            'sender': {'name': c.sender_name, 'email': c.sender_email},
            'received_date': c.received_date.strftime('%Y-%m-%d %H:%M:%S') if c.received_date else '',
            'preview': c.body_preview,
            'has_attachments': c.has_attachments,
            'importance': c.importance
        } for c in communications]
        
        # Générer le PDF
        exporter = PDFExporter()
        pdf_path = exporter.export_to_pdf(emails_data)
        
        return send_file(pdf_path, as_attachment=True, download_name=f'registre_communications_{datetime.now().strftime("%Y%m%d")}.pdf')
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/user/update-outlook', methods=['POST'])
@login_required
def update_outlook_config():
    """Met à jour la configuration Outlook de l'utilisateur"""
    data = request.json
    
    current_user.outlook_email = data.get('outlook_email')
    current_user.client_id = data.get('client_id')
    current_user.client_secret = data.get('client_secret')
    current_user.tenant_id = data.get('tenant_id')
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Configuration Outlook mise à jour'})


@app.route('/api/authenticate-outlook', methods=['POST'])
@login_required
def authenticate_outlook():
    """Authentifie avec Microsoft Graph API en utilisant la config de l'utilisateur"""
    if not current_user.has_outlook_config():
        return jsonify({
            'success': False,
            'error': 'Configuration Outlook manquante. Veuillez configurer votre compte dans votre profil.'
        }), 400
    
    try:
        # Utiliser la configuration de l'utilisateur
        auth = OutlookAuth()
        auth.client_id = current_user.client_id
        auth.client_secret = current_user.client_secret
        auth.authority = f'https://login.microsoftonline.com/{current_user.tenant_id}'
        
        token = auth.authenticate()
        
        # Stocker le token en session
        session['outlook_token'] = token
        session['outlook_token_expires'] = (datetime.utcnow() + timedelta(hours=1)).isoformat()
        
        return jsonify({
            'success': True,
            'message': 'Authentification Outlook réussie!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/fetch-communications', methods=['POST'])
@login_required
def fetch_communications():
    """Récupère les emails et les enregistre dans le registre des communications"""
    token = session.get('outlook_token')
    
    if not token:
        return jsonify({
            'success': False,
            'error': 'Non authentifié avec Outlook'
        }), 401
    
    try:
        data = request.json
        limit = data.get('limit', 100)
        
        fetcher = EmailFetcher(token)
        emails = fetcher.fetch_emails(limit=limit, user_email=current_user.outlook_email)
        
        # Enregistrer dans la base de données
        new_count = 0
        updated_count = 0
        
        for email_data in emails:
            # Vérifier si la communication existe déjà
            comm = Communication.query.filter_by(
                email_id=email_data['id'],
                user_id=current_user.id
            ).first()
            
            if not comm:
                # Créer une nouvelle communication
                comm = Communication(
                    user_id=current_user.id,
                    email_id=email_data['id']
                )
                new_count += 1
            else:
                updated_count += 1
            
            # Mettre à jour les données
            comm.subject = email_data.get('subject', '')
            comm.sender_name = email_data.get('sender', {}).get('name', '')
            comm.sender_email = email_data.get('sender', {}).get('email', '')
            comm.set_recipients(email_data.get('to', []))
            comm.set_cc_recipients(email_data.get('cc', []))
            
            # Parser la date
            date_str = email_data.get('received_date', '')
            try:
                comm.received_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except:
                comm.received_date = datetime.utcnow()
            
            comm.body_preview = email_data.get('preview', '')
            comm.has_attachments = email_data.get('has_attachments', False)
            comm.is_read = email_data.get('is_read', False)
            comm.importance = email_data.get('importance', 'normal')
            
            db.session.add(comm)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{new_count} nouvelles communications, {updated_count} mises à jour',
            'new': new_count,
            'updated': updated_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/communications')
@login_required
def get_communications():
    """Retourne les communications de l'utilisateur"""
    # Paramètres de filtrage et pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    importance = request.args.get('importance', '')
    is_read = request.args.get('is_read', '')
    
    # Construire la requête
    query = Communication.query.filter_by(user_id=current_user.id)
    
    # Filtres
    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            db.or_(
                Communication.subject.like(search_filter),
                Communication.sender_name.like(search_filter),
                Communication.sender_email.like(search_filter),
                Communication.body_preview.like(search_filter)
            )
        )
    
    if category:
        query = query.filter_by(category=category)
    
    if importance:
        query = query.filter_by(importance=importance)
    
    if is_read != '':
        query = query.filter_by(is_read=is_read == 'true')
    
    # Tri par date décroissante
    query = query.order_by(Communication.received_date.desc())
    
    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'communications': [comm.to_dict() for comm in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@app.route('/api/communications/<int:comm_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def communication_detail(comm_id):
    """Gérer une communication spécifique"""
    comm = Communication.query.filter_by(id=comm_id, user_id=current_user.id).first()
    
    if not comm:
        return jsonify({'success': False, 'error': 'Communication non trouvée'}), 404
    
    if request.method == 'GET':
        return jsonify({'success': True, 'communication': comm.to_dict()})
    
    elif request.method == 'PUT':
        # Mettre à jour la communication
        data = request.json
        
        if 'category' in data:
            comm.category = data['category']
        if 'tags' in data:
            comm.set_tags(data['tags'])
        if 'notes' in data:
            comm.notes = data['notes']
        if 'is_read' in data:
            comm.is_read = data['is_read']
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Communication mise à jour'})
    
    elif request.method == 'DELETE':
        db.session.delete(comm)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Communication supprimée'})


@app.route('/api/stats')
@login_required
def get_stats():
    """Retourne les statistiques de l'utilisateur"""
    total = Communication.query.filter_by(user_id=current_user.id).count()
    unread = Communication.query.filter_by(user_id=current_user.id, is_read=False).count()
    with_attachments = Communication.query.filter_by(user_id=current_user.id, has_attachments=True).count()
    important = Communication.query.filter_by(user_id=current_user.id, importance='high').count()
    
    # Communications des 7 derniers jours
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent = Communication.query.filter(
        Communication.user_id == current_user.id,
        Communication.received_date >= seven_days_ago
    ).count()
    
    # Top expéditeurs
    from sqlalchemy import func
    top_senders = db.session.query(
        Communication.sender_name,
        Communication.sender_email,
        func.count(Communication.id).label('count')
    ).filter(
        Communication.user_id == current_user.id
    ).group_by(
        Communication.sender_name, Communication.sender_email
    ).order_by(
        func.count(Communication.id).desc()
    ).limit(5).all()
    
    return jsonify({
        'success': True,
        'stats': {
            'total': total,
            'unread': unread,
            'with_attachments': with_attachments,
            'important': important,
            'recent_7days': recent,
            'top_senders': [
                {'name': s[0], 'email': s[1], 'count': s[2]}
                for s in top_senders
            ]
        }
    })


@app.route('/api/download-pdf/<filename>')
@login_required
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


def init_db():
    """Initialise la base de données"""
    with app.app_context():
        db.create_all()
        
        # Créer un utilisateur admin par défaut si aucun utilisateur n'existe
        if User.query.count() == 0:
            admin = User(
                username='admin',
                email='admin@rego.local',
                full_name='Administrateur',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("\n✅ Utilisateur admin créé: admin / admin123")


if __name__ == '__main__':
    init_db()
    
    print("\n" + "="*60)
    print("🚀 RegO - Dashboard Professionnel")
    print("="*60)
    print("🌐 Dashboard: http://localhost:5000")
    print("👤 Compte admin par défaut: admin / admin123")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
