"""
Service d'envoi d'emails pour les devis
"""
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def send_quote_email(quote, email_type='created', context=None):
    """
    Envoie un email pour un devis
    
    Args:
        quote: Instance du modèle Quote
        email_type: Type d'email ('created', 'accepted', 'rejected', 'reminder')
        context: Contexte additionnel pour le template
        
    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon
    """
    # Configuration des emails selon le type
    email_configs = {
        'created': {
            'subject': f'Votre devis {quote.quote_number} - ZsDevWeb',
            'template': 'emails/quote_created.html',
            'from_email': settings.DEFAULT_FROM_EMAIL,
        },
        'accepted': {
            'subject': f'Confirmation de signature - {quote.quote_number} - ZsDevWeb',
            'template': 'emails/quote_accepted.html',
            'from_email': settings.DEFAULT_FROM_EMAIL,
        },
        'rejected': {
            'subject': f'Accusé de réception - {quote.quote_number} - ZsDevWeb',
            'template': 'emails/quote_rejected.html',
            'from_email': settings.DEFAULT_FROM_EMAIL,
        },
        'reminder': {
            'subject': f'Rappel - Votre devis {quote.quote_number} expire bientôt - ZsDevWeb',
            'template': 'emails/quote_reminder.html',
            'from_email': settings.DEFAULT_FROM_EMAIL,
        }
    }
    
    # Vérifier que le type d'email est valide
    if email_type not in email_configs:
        logger.error(f"Type d'email invalide: {email_type}")
        return False
    
    config = email_configs[email_type]
    
    try:
        # Construire l'URL publique du devis
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
        quote_url = f"{frontend_url}/signature/{quote.public_token}"
        
        # Préparer le contexte pour le template
        email_context = {
            'quote': quote,
            'quote_url': quote_url,
            'current_year': timezone.now().year,
        }
        
        # Ajouter le contexte additionnel si fourni
        if context:
            email_context.update(context)
        
        # Pour les rappels, calculer les jours restants
        if email_type == 'reminder' and quote.valid_until:
            days_remaining = (quote.valid_until - timezone.now().date()).days
            email_context['days_remaining'] = max(0, days_remaining)
        
        # Rendre le template HTML
        html_content = render_to_string(config['template'], email_context)
        
        # Créer l'email
        email = EmailMultiAlternatives(
            subject=config['subject'],
            body='',  # Le corps texte sera vide, on utilise uniquement HTML
            from_email=config['from_email'],
            to=[quote.client_email],
            reply_to=[config['from_email']],
        )
        
        # Attacher la version HTML
        email.attach_alternative(html_content, "text/html")
        
        # Envoyer l'email
        email.send(fail_silently=False)
        
        logger.info(
            f"Email '{email_type}' envoyé avec succès pour le devis {quote.quote_number} "
            f"à {quote.client_email}"
        )
        
        return True
        
    except Exception as e:
        logger.error(
            f"Erreur lors de l'envoi de l'email '{email_type}' pour le devis "
            f"{quote.quote_number}: {str(e)}"
        )
        return False


def send_quote_created_email(quote):
    """Envoie l'email de création de devis"""
    return send_quote_email(quote, email_type='created')


def send_quote_accepted_email(quote):
    """Envoie l'email de confirmation de signature"""
    return send_quote_email(quote, email_type='accepted')


def send_quote_rejected_email(quote):
    """Envoie l'email d'accusé de réception de refus"""
    return send_quote_email(quote, email_type='rejected')


def send_quote_reminder_email(quote):
    """Envoie l'email de rappel avant expiration"""
    return send_quote_email(quote, email_type='reminder')