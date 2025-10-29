"""
Générateur de PDF Premium pour les devis
Inclut : logo, remises, signature électronique, conditions de paiement
"""
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from django.conf import settings
from datetime import datetime
import os


class QuotePDFGenerator:
    """Générateur de PDF professionnel pour les devis Premium"""
    
    def __init__(self, quote):
        self.quote = quote
        self.buffer = BytesIO()
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Récupérer les infos de l'entreprise
        from .models import Company
        self.company = Company.get_instance()
    
    def _setup_custom_styles(self):
        """Définir des styles personnalisés"""
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1a56db'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
        ))
        
        # Sous-titre
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a56db'),
            spaceAfter=10,
            fontName='Helvetica-Bold',
        ))
        
        # Texte normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14,
        ))
        
        # Texte petit
        self.styles.add(ParagraphStyle(
            name='SmallText',
            parent=self.styles['Normal'],
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#6b7280'),
        ))
    
    def generate(self):
        """Génère le PDF complet"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )
        
        # Construire le contenu
        story = []
        
        # Logo et en-tête
        story.extend(self._build_logo_and_header())
        story.append(Spacer(1, 0.5*cm))
        
        # Informations du devis
        story.extend(self._build_quote_info())
        story.append(Spacer(1, 0.5*cm))
        
        # Informations client
        story.extend(self._build_client_info())
        story.append(Spacer(1, 0.5*cm))
        
        # Description du projet
        story.extend(self._build_project_description())
        story.append(Spacer(1, 0.5*cm))
        
        # Détails du devis
        story.extend(self._build_quote_details())
        story.append(Spacer(1, 0.5*cm))
        
        # Remise (si applicable)
        if self.quote.discount_value > 0:
            story.extend(self._build_discount_section())
            story.append(Spacer(1, 0.3*cm))
        
        # Totaux
        story.extend(self._build_totals())
        story.append(Spacer(1, 0.5*cm))
        
        # Conditions de paiement
        story.extend(self._build_payment_terms())
        story.append(Spacer(1, 0.5*cm))
        
        # Durée et dates
        story.extend(self._build_timeline())
        story.append(Spacer(1, 0.5*cm))
        
        # Conditions générales
        story.extend(self._build_terms())
        story.append(Spacer(1, 0.5*cm))
        
        # Signature
        story.extend(self._build_signature_section())
        
        # Générer le PDF
        doc.build(story)
        
        # Retourner le buffer
        self.buffer.seek(0)
        return self.buffer
    
    def _build_logo_and_header(self):
        """Logo et en-tête de l'entreprise"""
        elements = []
        
        # Essayer d'ajouter le logo
        if self.company.logo:
            try:
                logo_path = self.company.logo.path
                if os.path.exists(logo_path):
                    img = Image(logo_path, width=6*cm, height=2*cm, kind='proportional')
                    elements.append(img)
                    elements.append(Spacer(1, 0.3*cm))
            except:
                pass
        
        # Titre avec le nom de l'entreprise
        title = Paragraph(self.company.name, self.styles['CustomTitle'])
        elements.append(title)
        
        # Coordonnées de l'entreprise
        company_info = f"""
        <para alignment="center" fontSize="9" textColor="#6b7280">
        {self.company.address.replace(chr(10), ' | ') if self.company.address else ''}<br/>
        {self.company.email} | {self.company.phone}<br/>
        SIRET: {self.company.siret} | TVA: {self.company.tva_number}
        </para>
        """
        elements.append(Paragraph(company_info, self.styles['SmallText']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Ligne de séparation
        line_data = [['', '']]
        line_table = Table(line_data, colWidths=[17*cm])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#1a56db')),
        ]))
        elements.append(line_table)
        
        return elements
    
    def _build_quote_info(self):
        """Informations du devis"""
        elements = []
        
        # Titre DEVIS en gros
        devis_title = Paragraph("DEVIS", self.styles['CustomTitle'])
        elements.append(devis_title)
        
        # Informations du devis dans un tableau
        data = [
            ['Numéro de devis:', self.quote.quote_number],
            ['Date d\'émission:', datetime.now().strftime('%d/%m/%Y')],
            ['Validité:', f"Jusqu'au {self.quote.expires_at.strftime('%d/%m/%Y')}" if self.quote.expires_at else '30 jours'],
        ]
        
        table = Table(data, colWidths=[5*cm, 12*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        elements.append(table)
        return elements
    
    def _build_client_info(self):
        """Informations client"""
        elements = []
        
        subtitle = Paragraph("INFORMATIONS CLIENT", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        client_data = [
            ['Nom:', self.quote.client_name],
            ['Email:', self.quote.client_email],
        ]
        
        if self.quote.client_phone:
            client_data.append(['Téléphone:', self.quote.client_phone])
        
        if self.quote.company_name:
            client_data.append(['Entreprise:', self.quote.company_name])
        
        if self.quote.client_address:
            client_data.append(['Adresse:', self.quote.client_address])
        
        table = Table(client_data, colWidths=[4*cm, 13*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(table)
        return elements
    
    def _build_project_description(self):
        """Description du projet"""
        elements = []
        
        subtitle = Paragraph("DESCRIPTION DU PROJET", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        # Type de projet
        project_info = f"<b>Type de projet :</b> {self.quote.project_type.name}"
        elements.append(Paragraph(project_info, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*cm))
        
        # Description
        description = Paragraph(self.quote.project_description, self.styles['CustomBody'])
        elements.append(description)
        
        return elements
    
    def _build_quote_details(self):
        """Détails du devis"""
        elements = []
        
        subtitle = Paragraph("DÉTAIL DU DEVIS", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        # En-tête du tableau
        data = [
            ['Désignation', 'Quantité', 'Prix unitaire HT', 'Total HT'],
        ]
        
        # Type de projet
        data.append([
            f"{self.quote.project_type.name}",
            '1',
            f"{self.quote.project_type.base_price:.2f} €",
            f"{self.quote.project_type.base_price:.2f} €"
        ])
        
        # Option de design
        data.append([
            f"Design {self.quote.design_option.name}",
            '1',
            f"{self.quote.design_option.price_supplement:.2f} €",
            f"{self.quote.design_option.price_supplement:.2f} €"
        ])
        
        # Niveau de complexité
        data.append([
            f"Complexité {self.quote.complexity_level.name} (×{self.quote.complexity_level.price_multiplier})",
            '1',
            'Multiplicateur',
            f"×{self.quote.complexity_level.price_multiplier}"
        ])
        
        # Options supplémentaires
        for option in self.quote.supplementary_options.all():
            billing_label = dict(option.BILLING_TYPE_CHOICES).get(option.billing_type, '')
            data.append([
                f"{option.name}\n({billing_label})",
                '1',
                f"{option.price:.2f} €",
                f"{option.price:.2f} €" if option.billing_type == 'one_time' else f"{option.price:.2f} €/{billing_label.lower()}"
            ])
        
        # Créer le tableau
        table = Table(data, colWidths=[8*cm, 2*cm, 3.5*cm, 3.5*cm])
        table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a56db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Corps du tableau
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Bordures
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_discount_section(self):
        """Section remise"""
        elements = []
        
        discount_text = f"<b>Remise appliquée :</b> "
        if self.quote.discount_type == 'percent':
            discount_text += f"{self.quote.discount_value:.0f}%"
        else:
            discount_text += f"{self.quote.discount_value:.2f} €"
        
        if self.quote.discount_reason:
            discount_text += f" ({self.quote.discount_reason})"
        
        discount_para = Paragraph(discount_text, self.styles['CustomBody'])
        elements.append(discount_para)
        
        return elements
    
    def _build_totals(self):
        """Totaux du devis"""
        elements = []
        
        subtitle = Paragraph("RÉCAPITULATIF", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        data = [
            ['Sous-total HT', f"{self.quote.subtotal_ht:.2f} €"],
        ]
        
        # Ajouter la ligne de remise si applicable
        if self.quote.discount_value > 0:
            data.append([
                f'Remise ({self.quote.discount_value:.0f}% )' if self.quote.discount_type == 'percent' else 'Remise',
                f"- {self.quote.discount_amount:.2f} €"
            ])
            data.append([
                'Total après remise HT',
                f"{self.quote.subtotal_ht - self.quote.discount_amount:.2f} €"
            ])
        
        data.extend([
            [f'TVA ({self.quote.tva_rate:.0f}%)', f"{self.quote.tva_amount:.2f} €"],
            ['TOTAL TTC', f"{self.quote.total_ttc:.2f} €"],
        ])
        
        table = Table(data, colWidths=[13.5*cm, 3.5*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -2), 11),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#1a56db')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#1a56db')),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.HexColor('#1a56db')),
        ]))
        
        elements.append(table)
        return elements
    
    def _build_payment_terms(self):
        """Conditions de paiement"""
        elements = []
        
        subtitle = Paragraph("CONDITIONS DE PAIEMENT", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        text = Paragraph(
            "Le paiement s'effectuera en <b>3 fois</b> selon l'échéancier suivant :",
            self.styles['CustomBody']
        )
        elements.append(text)
        elements.append(Spacer(1, 0.3*cm))
        
        data = [
            ['🔹 30% à la signature du devis', f"{self.quote.payment_first:.2f} €"],
            ['🔹 40% à mi-parcours du projet', f"{self.quote.payment_second:.2f} €"],
            ['🔹 30% à la livraison finale', f"{self.quote.payment_final:.2f} €"],
        ]
        
        table = Table(data, colWidths=[13.5*cm, 3.5*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(table)
        return elements
    
    def _build_timeline(self):
        """Durée et dates estimées"""
        elements = []
        
        subtitle = Paragraph("PLANNING PRÉVISIONNEL", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        timeline_text = f"<b>Durée estimée :</b> {self.quote.estimated_duration_days} jours ouvrés"
        
        if self.quote.estimated_start_date:
            timeline_text += f"<br/><b>Date de début estimée :</b> {self.quote.estimated_start_date.strftime('%d/%m/%Y')}"
        
        if self.quote.estimated_end_date:
            timeline_text += f"<br/><b>Date de livraison estimée :</b> {self.quote.estimated_end_date.strftime('%d/%m/%Y')}"
        
        timeline_para = Paragraph(timeline_text, self.styles['CustomBody'])
        elements.append(timeline_para)
        
        return elements
    
    def _build_terms(self):
        """Conditions générales"""
        elements = []
        
        subtitle = Paragraph("CONDITIONS GÉNÉRALES", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        terms_text = """
        <b>Validité du devis :</b> Ce devis est valable 30 jours à compter de sa date d'émission.<br/>
        <br/>
        <b>Délai de réalisation :</b> Le délai indiqué est une estimation et peut varier en fonction 
        de la complexité du projet et de la réactivité du client dans la fourniture des éléments nécessaires.<br/>
        <br/>
        <b>Révisions :</b> Deux révisions majeures sont incluses dans le prix. 
        Toute révision supplémentaire sera facturée en supplément à hauteur de 80€/heure.<br/>
        <br/>
        <b>Propriété intellectuelle :</b> Les droits de propriété intellectuelle sont transférés 
        au client après paiement complet du projet.<br/>
        <br/>
        <b>Résiliation :</b> En cas d'annulation par le client, les montants déjà versés restent acquis 
        à titre d'indemnité pour les travaux déjà effectués.<br/>
        <br/>
        <b>Garantie :</b> Une garantie de 3 mois contre les bugs est incluse après la livraison finale.
        """
        
        terms = Paragraph(terms_text, self.styles['CustomBody'])
        elements.append(terms)
        
        return elements
    
    def _build_signature_section(self):
        """Section signature"""
        elements = []
        
        elements.append(Spacer(1, 1*cm))
        
        # Deux colonnes : entreprise et client
        signature_data = [
            ['Pour l\'entreprise', 'Bon pour accord, le client'],
            [self.company.name, ''],
            ['', ''],
            ['', 'Signature précédée de "Lu et approuvé" :'],
        ]
        
        table = Table(signature_data, colWidths=[8.5*cm, 8.5*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(table)
        
        # Footer
        elements.append(Spacer(1, 1*cm))
        footer = Paragraph(
            self.company.footer_text,
            self.styles['SmallText']
        )
        elements.append(footer)
        
        return elements