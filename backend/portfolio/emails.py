"""
Service d'envoi d'emails pour les messages de contact
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_contact_notification_email(contact_message):
    """
    Envoie un email de notification à l'admin quand un nouveau message de contact arrive

    Args:
        contact_message: Instance de ContactMessage
    """
    # Sujet de l'email
    subject = f'📬 Nouveau message de contact - {contact_message.subject}'

    # Contexte pour le template
    context = {
        'message': contact_message,
        'admin_url': f'{settings.FRONTEND_URL}/admin',  # URL pour gérer les messages
    }

    # Rendre le template HTML
    html_content = render_to_string('emails/contact_notification.html', context)

    # Version texte simple (fallback)
    text_content = f"""
Nouveau message de contact reçu !

De : {contact_message.name} ({contact_message.email})
Téléphone : {contact_message.phone or 'Non fourni'}
Sujet : {contact_message.subject}

Message :
{contact_message.message}

Répondre à : {contact_message.email}
    """

    # Créer l'email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.EMAIL_HOST_USER],  # Envoyer à votre propre email
        reply_to=[contact_message.email],  # Pour pouvoir répondre directement
    )
    email.attach_alternative(html_content, "text/html")

    # Envoyer
    try:
        email.send()
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de la notification: {e}")
        raise


def send_contact_auto_reply(contact_message):
    """
    Envoie un email de confirmation automatique au visiteur

    Args:
        contact_message: Instance de ContactMessage
    """
    # Sujet de l'email
    subject = f'✅ Confirmation de réception - {contact_message.subject}'

    # Contexte pour le template
    context = {
        'message': contact_message,
        'frontend_url': settings.FRONTEND_URL,
    }

    # Rendre le template HTML
    html_content = render_to_string('emails/contact_auto_reply.html', context)

    # Version texte simple (fallback)
    text_content = f"""
Bonjour {contact_message.name},

Nous avons bien reçu votre message concernant : "{contact_message.subject}".

Nous vous répondrons dans les plus brefs délais (généralement sous 24-48h).

Cordialement,
L'équipe ZsDevWeb
    """

    # Créer l'email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[contact_message.email],
    )
    email.attach_alternative(html_content, "text/html")

    # Envoyer
    try:
        email.send()
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de la confirmation: {e}")
        raise
