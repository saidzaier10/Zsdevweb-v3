"""
Service de génération et gestion des PDFs pour les devis
"""
import logging
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponse
from ..pdf_generator_weasy import QuotePDFGeneratorWeasy
from ..utils.decorators import log_quote_action
from ..utils.constants import ErrorMessages

logger = logging.getLogger(__name__)


class PDFService:
    """Service pour gérer la génération des PDFs de devis"""

    @staticmethod
    @log_quote_action("Génération et sauvegarde du PDF")
    def generate_and_save_pdf(quote) -> bool:
        """
        Génère un PDF pour le devis et le sauvegarde dans le modèle

        Args:
            quote: Instance du modèle Quote

        Returns:
            True si la génération a réussi, False sinon

        Raises:
            Exception: Si une erreur critique se produit
        """
        try:
            generator = QuotePDFGeneratorWeasy(quote)
            pdf_buffer = generator.generate()
            pdf_content = pdf_buffer.getvalue()

            # Sauvegarder le PDF dans le modèle
            filename = f'devis_{quote.quote_number}.pdf'
            quote.pdf_file.save(
                filename,
                ContentFile(pdf_content),
                save=True
            )

            logger.info(f"PDF généré avec succès: {filename}")
            return True

        except Exception as e:
            logger.error(f"Erreur lors de la génération du PDF pour le devis {quote.id}: {str(e)}", exc_info=True)
            raise Exception(ErrorMessages.PDF_GENERATION_ERROR) from e

    @staticmethod
    @log_quote_action("Génération du PDF pour téléchargement")
    def generate_pdf_response(quote) -> HttpResponse:
        """
        Génère un PDF et retourne une réponse HTTP pour le téléchargement

        Args:
            quote: Instance du modèle Quote

        Returns:
            HttpResponse contenant le PDF

        Raises:
            Exception: Si une erreur se produit lors de la génération
        """
        try:
            # Générer le PDF
            generator = QuotePDFGeneratorWeasy(quote)
            pdf_buffer = generator.generate()
            pdf_content = pdf_buffer.getvalue()

            # Sauvegarder dans le modèle pour garder une copie
            filename = f'devis_{quote.quote_number}.pdf'
            quote.pdf_file.save(
                filename,
                ContentFile(pdf_content),
                save=True
            )

            # Créer la réponse HTTP
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            logger.info(f"PDF généré et prêt pour téléchargement: {filename}")
            return response

        except Exception as e:
            logger.error(f"Erreur lors de la génération du PDF pour téléchargement (devis {quote.id}): {str(e)}", exc_info=True)
            raise Exception(ErrorMessages.PDF_GENERATION_ERROR) from e

    @staticmethod
    def get_pdf_buffer(quote) -> BytesIO:
        """
        Génère un PDF et retourne le buffer pour utilisation (ex: email attachment)

        Args:
            quote: Instance du modèle Quote

        Returns:
            BytesIO buffer contenant le PDF

        Raises:
            Exception: Si une erreur se produit lors de la génération
        """
        try:
            generator = QuotePDFGeneratorWeasy(quote)
            pdf_buffer = generator.generate()

            logger.debug(f"PDF buffer généré pour le devis {quote.id}")
            return pdf_buffer

        except Exception as e:
            logger.error(f"Erreur lors de la génération du buffer PDF (devis {quote.id}): {str(e)}", exc_info=True)
            raise Exception(ErrorMessages.PDF_GENERATION_ERROR) from e
