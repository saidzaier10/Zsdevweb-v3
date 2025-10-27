from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modèle utilisateur personnalisé"""
    
    USER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('admin', 'Administrateur'),
    ]
    
    # Informations supplémentaires
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    
    # Avatar
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Préférences
    email_notifications = models.BooleanField(default=True, help_text="Recevoir les notifications par email")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_client(self):
        """Vérifie si l'utilisateur est un client"""
        return self.user_type == 'client'

    @property
    def is_admin_user(self):
        """Vérifie si l'utilisateur est un admin"""
        return self.user_type == 'admin' or self.is_superuser
