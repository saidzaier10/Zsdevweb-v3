"""
Service d'envoi d'emails pour les devis
"""
import logging
from django.utils import timezone
from ..emails import (
    send_quote_created_email,
    send_quote_accepted_email,
    send_quote_rejected_email,
    send_quote_reminder_email,
)
from ..utils.decorators import log_quote_action
from ..utils.constants import (
    EmailType,
    ErrorMessages,
    SuccessMessages,
    QuoteStatus,
)

logger = logging.getLogger(__name__)


class EmailService:
    """Service pour gérer l'envoi des emails de devis"""

    @staticmethod
    @log_quote_action("Envoi de l'email de création")
    def send_created_email(quote) -> bool:
        """
        Envoie l'email de création de devis au client

        Args:
            quote: Instance du modèle Quote

        Returns:
            True si l'envoi a réussi

        Raises:
            Exception: Si l'envoi échoue
        """
        try:
            send_quote_created_email(quote)
            logger.info(f"Email de création envoyé pour le devis {quote.id} à {quote.client_email}")
            return True
        except Exception as e:
            logger.error(f"Échec de l'envoi de l'email de création pour le devis {quote.id}: {str(e)}", exc_info=True)
            raise Exception(ErrorMessages.EMAIL_SEND_ERROR) from e

    @staticmethod
    @log_quote_action("Envoi de l'email d'acceptation")
    def send_accepted_email(quote) -> bool:
        """
        Envoie l'email de confirmation de signature au client et à l'admin

        Args:
            quote: Instance du modèle Quote

        Returns:
            True si l'envoi a réussi

        Raises:
            Exception: Si l'envoi échoue
        """
        try:
            send_quote_accepted_email(quote)
            logger.info(f"Email d'acceptation envoyé pour le devis {quote.id}")
            return True
        except Exception as e:
            logger.error(f"Échec de l'envoi de l'email d'acceptation pour le devis {quote.id}: {str(e)}", exc_info=True)
            # On log mais on ne bloque pas le processus de signature
            # L'email admin peut échouer sans bloquer la signature
            logger.warning(f"L'envoi de l'email a échoué mais la signature a été enregistrée")
            return False

    @staticmethod
    @log_quote_action("Envoi de l'email de refus")
    def send_rejected_email(quote) -> bool:
        """
        Envoie l'email d'accusé de réception de refus

        Args:
            quote: Instance du modèle Quote

        Returns:
            True si l'envoi a réussi

        Raises:
            Exception: Si l'envoi échoue
        """
        try:
            send_quote_rejected_email(quote)
            logger.info(f"Email de refus envoyé pour le devis {quote.id}")
            return True
        except Exception as e:
            logger.error(f"Échec de l'envoi de l'email de refus pour le devis {quote.id}: {str(e)}", exc_info=True)
            # On log mais on ne bloque pas le processus de refus
            return False

    @staticmethod
    @log_quote_action("Envoi de l'email de rappel")
    def send_reminder_email(quote) -> bool:
        """
        Envoie un email de rappel pour un devis qui expire bientôt

        Args:
            quote: Instance du modèle Quote

        Returns:
            True si l'envoi a réussi

        Raises:
            Exception: Si l'envoi échoue
        """
        try:
            send_quote_reminder_email(quote)
            logger.info(f"Email de rappel envoyé pour le devis {quote.id}")
            return True
        except Exception as e:
            logger.error(f"Échec de l'envoi de l'email de rappel pour le devis {quote.id}: {str(e)}", exc_info=True)
            return False

    @staticmethod
    def send_email_with_status_update(quote, email_type: str) -> bool:
        """
        Envoie un email et met à jour le statut du devis si nécessaire

        Args:
            quote: Instance du modèle Quote
            email_type: Type d'email à envoyer (EmailType constant)

        Returns:
            True si l'envoi a réussi

        Raises:
            ValueError: Si le type d'email est invalide
            Exception: Si l'envoi échoue
        """
        # Mapper le type d'email à la fonction d'envoi
        email_senders = {
            EmailType.CREATED: EmailService.send_created_email,
            EmailType.ACCEPTED: EmailService.send_accepted_email,
            EmailType.REJECTED: EmailService.send_rejected_email,
            EmailType.REMINDER: EmailService.send_reminder_email,
        }

        sender = email_senders.get(email_type)
        if not sender:
            raise ValueError(f"Type d'email invalide: {email_type}")

        # Envoyer l'email
        success = sender(quote)

        # Mettre à jour le statut si c'est un email de création
        if success and email_type == EmailType.CREATED:
            if quote.status == QuoteStatus.DRAFT:
                quote.status = QuoteStatus.SENT
                quote.sent_at = timezone.now()
                quote.save(update_fields=['status', 'sent_at'])
                logger.info(f"Statut du devis {quote.id} mis à jour à 'sent'")

        return success
