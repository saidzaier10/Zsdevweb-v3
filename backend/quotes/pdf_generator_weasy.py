"""
Générateur de PDF avec WeasyPrint
Utilise des templates HTML/CSS pour créer des PDF professionnels
"""
from io import BytesIO
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


class QuotePDFGeneratorWeasy:
    """Générateur de PDF utilisant WeasyPrint et templates HTML"""

    def __init__(self, quote):
        self.quote = quote

        # Récupérer les infos de l'entreprise
        from .models import Company
        self.company = Company.get_instance()

    def generate(self):
        """
        Génère le PDF à partir du template HTML

        Returns:
            BytesIO: Buffer contenant le PDF généré
        """
        # Préparer le contexte pour le template
        context = {
            'quote': self.quote,
            'company': self.company,
            'today': timezone.now(),
        }

        # Rendre le template HTML
        html_string = render_to_string('quotes/quote_pdf.html', context)

        # Configuration des polices
        font_config = FontConfiguration()

        # Générer le PDF à partir du HTML
        html = HTML(string=html_string)

        # CSS supplémentaire optionnel (si besoin)
        # css = CSS(string='@page { size: A4; margin: 2cm; }')

        # Générer le PDF dans un buffer
        pdf_buffer = BytesIO()
        html.write_pdf(pdf_buffer, font_config=font_config)

        # Retourner au début du buffer
        pdf_buffer.seek(0)

        return pdf_buffer
