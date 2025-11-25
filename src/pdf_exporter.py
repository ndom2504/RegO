"""
Module pour exporter le registre en PDF avec un design élégant
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import List, Dict
import os
from config.settings import Config


class PDFExporter:
    """Exporte le registre des emails en PDF avec un design professionnel"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Crée des styles personnalisés pour le PDF"""
        
        # Style pour le titre principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Style pour les sous-titres
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Style pour le sujet de l'email
        self.styles.add(ParagraphStyle(
            name='EmailSubject',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#0d47a1'),
            fontName='Helvetica-Bold',
            spaceAfter=6
        ))
        
        # Style pour les détails
        self.styles.add(ParagraphStyle(
            name='EmailDetails',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#424242'),
            leftIndent=20
        ))
        
        # Style pour le preview
        self.styles.add(ParagraphStyle(
            name='EmailPreview',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#616161'),
            leftIndent=20,
            spaceAfter=10,
            fontName='Helvetica-Oblique'
        ))
    
    def export_to_pdf(self, emails: List[Dict], output_path: str = None, user_info: Dict = None) -> str:
        """
        Exporte les emails en PDF
        
        Args:
            emails: Liste des emails à exporter
            output_path: Chemin du fichier PDF de sortie
            user_info: Informations sur l'utilisateur
        
        Returns:
            Chemin du fichier PDF créé
        """
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(Config.EXPORTS_DIR, f'registre_emails_{timestamp}.pdf')
        
        # Créer le dossier exports si nécessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Créer le document PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        # Conteneur pour les éléments du PDF
        elements = []
        
        # Ajouter l'en-tête
        elements.extend(self._create_header(len(emails), user_info))
        
        # Ajouter les statistiques
        elements.extend(self._create_stats(emails))
        
        elements.append(PageBreak())
        
        # Ajouter chaque email
        for idx, email in enumerate(emails, 1):
            elements.extend(self._create_email_entry(email, idx))
            
            # Ajouter un saut de page tous les 3 emails pour une meilleure lisibilité
            if idx % 3 == 0 and idx < len(emails):
                elements.append(PageBreak())
        
        # Générer le PDF
        doc.build(elements)
        
        return output_path
    
    def _create_header(self, email_count: int, user_info: Dict = None) -> List:
        """Crée l'en-tête du document"""
        elements = []
        
        # Titre principal
        title = Paragraph("📧 Registre des Courriels Outlook", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Informations utilisateur si disponibles
        if user_info:
            user_name = user_info.get('name', 'Utilisateur')
            user_email = user_info.get('email', '')
            user_text = f"<b>Utilisateur:</b> {user_name}"
            if user_email:
                user_text += f" ({user_email})"
            elements.append(Paragraph(user_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Date de génération
        date_text = f"<b>Date de génération:</b> {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        elements.append(Paragraph(date_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Nombre d'emails
        count_text = f"<b>Nombre total de courriels:</b> {email_count}"
        elements.append(Paragraph(count_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_stats(self, emails: List[Dict]) -> List:
        """Crée une section de statistiques"""
        elements = []
        
        # Titre de la section
        elements.append(Paragraph("📊 Statistiques", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Calculer les stats
        total = len(emails)
        read = sum(1 for e in emails if e.get('is_read'))
        unread = total - read
        with_attachments = sum(1 for e in emails if e.get('has_attachments'))
        important = sum(1 for e in emails if e.get('importance') == 'high')
        
        # Créer un tableau de stats
        data = [
            ['Statut', 'Nombre'],
            ['Total', str(total)],
            ['Lus', str(read)],
            ['Non lus', str(unread)],
            ['Avec pièces jointes', str(with_attachments)],
            ['Importants', str(important)]
        ]
        
        table = Table(data, colWidths=[3*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e3f2fd')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#90caf9')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_email_entry(self, email: Dict, index: int) -> List:
        """Crée une entrée pour un email"""
        elements = []
        
        # Numéro et sujet
        subject = email.get('subject', '(Pas de sujet)')
        subject_text = f"<b>#{index}</b> - {self._escape_html(subject)}"
        elements.append(Paragraph(subject_text, self.styles['EmailSubject']))
        
        # Créer un tableau pour les détails
        sender = email.get('sender', {})
        sender_name = sender.get('name', 'Inconnu')
        sender_email = sender.get('email', '')
        
        details_data = [
            ['De:', f"{sender_name} <{sender_email}>"],
            ['Date:', email.get('received_date', 'Date inconnue')],
        ]
        
        # Ajouter les destinataires
        to_recipients = email.get('to', [])
        if to_recipients:
            to_list = ', '.join([f"{r.get('name', '')} <{r.get('email', '')}>" for r in to_recipients[:3]])
            if len(to_recipients) > 3:
                to_list += f" (+{len(to_recipients)-3} autres)"
            details_data.append(['À:', to_list])
        
        # Ajouter les CC si présents
        cc_recipients = email.get('cc', [])
        if cc_recipients:
            cc_list = ', '.join([f"{r.get('name', '')} <{r.get('email', '')}>" for r in cc_recipients[:2]])
            if len(cc_recipients) > 2:
                cc_list += f" (+{len(cc_recipients)-2} autres)"
            details_data.append(['CC:', cc_list])
        
        # Statut
        status_parts = []
        if email.get('is_read'):
            status_parts.append('✓ Lu')
        else:
            status_parts.append('✉ Non lu')
        
        if email.get('has_attachments'):
            status_parts.append('📎 Pièces jointes')
        
        if email.get('importance') == 'high':
            status_parts.append('⚠ Important')
        
        details_data.append(['Statut:', ' | '.join(status_parts)])
        
        # Créer le tableau
        details_table = Table(details_data, colWidths=[1*inch, 4.5*inch])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#424242')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#616161')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ]))
        
        elements.append(details_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Aperçu du contenu
        preview = email.get('preview', '')
        if preview:
            preview_text = f"<i>{self._escape_html(preview)}</i>"
            elements.append(Paragraph(preview_text, self.styles['EmailPreview']))
        
        # Ligne de séparation
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Table([['']], colWidths=[6.5*inch], style=TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#e0e0e0'))
        ])))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _escape_html(self, text: str) -> str:
        """Échappe les caractères HTML spéciaux"""
        if not text:
            return ''
        text = str(text)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text
