"""
Service d'envoi d'emails pour les devis
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


def send_quote_email(quote, email_type='created', context=None):
    """
    Envoie un email pour un devis
    
    Args:
        quote: Instance du devis
        email_type: Type d'email ('created', 'accepted', 'rejected', 'reminder')
        context: Contexte additionnel pour le template
    """
    if context is None:
        context = {}
    
    # Configuration selon le type d'email
    email_configs = {
        'created': {
            'subject': f'Votre devis {quote.quote_number} - ZsDevWeb',
            'template': 'emails/quote_created.html',
        },
        'accepted': {
            'subject': f'Confirmation de signature - Devis {quote.quote_number}',
            'template': 'emails/quote_accepted.html',
        },
        'rejected': {
            'subject': f'Accusé de réception - Devis {quote.quote_number}',
            'template': 'emails/quote_rejected.html',
        },
        'reminder': {
            'subject': f'Rappel - Votre devis {quote.quote_number} expire bientôt',
            'template': 'emails/quote_reminder.html',
        },
    }
    
    config = email_configs.get(email_type)
    if not config:
        raise ValueError(f"Type d'email invalide: {email_type}")
    
    # Préparer le contexte
    email_context = {
        'quote': quote,
        'frontend_url': settings.FRONTEND_URL,
        'signature_link': f"{settings.FRONTEND_URL}/signature/{quote.signature_token}",
        'current_year': timezone.now().year,
        **context
    }
    
    # Ajouter le nombre de jours restants pour les rappels
    if email_type == 'reminder' and quote.expires_at:
        days_remaining = (quote.expires_at - timezone.now()).days
        email_context['days_remaining'] = max(0, days_remaining)
    
    # Rendre le template HTML
    html_content = render_to_string(config['template'], email_context)

    # Créer l'email
    email = EmailMultiAlternatives(
        subject=config['subject'],
        body=f"Veuillez consulter ce message au format HTML.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[quote.client_email],
    )
    email.attach_alternative(html_content, "text/html")

    # Attacher le PDF si disponible (pour les devis créés ou rappels)
    if email_type in ['created', 'reminder'] and quote.pdf_file:
        try:
            email.attach_file(quote.pdf_file.path)
        except Exception as e:
            print(f"⚠️ Impossible d'attacher le PDF: {e}")

    # Envoyer
    try:
        email.send()
        
        # Logger l'envoi
        from .models import QuoteEmailLog
        QuoteEmailLog.objects.create(
            quote=quote,
            email_type=email_type,
            recipient=quote.client_email,
            subject=config['subject'],
            success=True
        )
        
        return True
    except Exception as e:
        # Logger l'échec
        from .models import QuoteEmailLog
        QuoteEmailLog.objects.create(
            quote=quote,
            email_type=email_type,
            recipient=quote.client_email,
            subject=config['subject'],
            success=False,
            error_message=str(e)
        )
        
        raise


def send_quote_created_email(quote):
    """Envoie l'email de création de devis"""
    return send_quote_email(quote, 'created')


def send_quote_accepted_email(quote):
    """Envoie l'email de confirmation de signature au client ET à l'admin"""
    # Email au client
    send_quote_email(quote, 'accepted')

    # Email spécifique à l'admin
    admin_email_context = {
        'quote': quote,
        'frontend_url': settings.FRONTEND_URL,
        'current_year': timezone.now().year,
    }

    html_content = render_to_string('emails/quote_accepted_admin.html', admin_email_context)

    admin_email = EmailMultiAlternatives(
        subject=f'🎉 Nouveau devis signé - {quote.quote_number}',
        body=f"Le devis {quote.quote_number} a été signé par {quote.signer_name}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_FROM_EMAIL],
    )
    admin_email.attach_alternative(html_content, "text/html")

    try:
        admin_email.send()

        # Logger l'envoi
        from .models import QuoteEmailLog
        QuoteEmailLog.objects.create(
            quote=quote,
            email_type='accepted_admin',
            recipient=settings.DEFAULT_FROM_EMAIL,
            subject=f'Nouveau devis signé - {quote.quote_number}',
            success=True
        )
    except Exception as e:
        print(f"⚠️ Erreur envoi email admin: {e}")

    return True


def send_quote_rejected_email(quote):
    """Envoie l'email d'accusé de réception de refus"""
    return send_quote_email(quote, 'rejected')


def send_quote_reminder_email(quote):
    """Envoie un email de rappel pour un devis qui expire bientôt"""
    return send_quote_email(quote, 'reminder')


def send_expiring_quotes_reminders():
    """
    Envoie des rappels pour tous les devis qui expirent dans 3 jours
    
    À utiliser dans une tâche cron/celery quotidienne
    """
    from .models import Quote
    
    three_days_from_now = timezone.now() + timedelta(days=3)
    expiring_quotes = Quote.objects.filter(
        status__in=['sent', 'viewed'],
        expires_at__date=three_days_from_now.date()
    )
    
    sent_count = 0
    failed_count = 0
    
    for quote in expiring_quotes:
        try:
            send_quote_reminder_email(quote)
            sent_count += 1
        except Exception:
            failed_count += 1
    
    return {
        'sent': sent_count,
        'failed': failed_count,
        'total': expiring_quotes.count()
    }