from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import secrets
import string

User = get_user_model()


class Company(models.Model):
    """Informations de l'entreprise (pour personnalisation des devis)"""
    name = models.CharField(max_length=200, default="Zsdevweb")
    logo = models.ImageField(upload_to='company/logos/', blank=True, null=True)
    email = models.EmailField(default="contact@zsdevweb.com")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    siret = models.CharField(max_length=14, blank=True)
    tva_number = models.CharField(max_length=20, blank=True, verbose_name="Numéro TVA")
    
    # Personnalisation PDF
    primary_color = models.CharField(max_length=7, default="#1a56db", help_text="Couleur hexadécimale")
    footer_text = models.TextField(
        blank=True,
        default="Merci de votre confiance | www.zsdevweb.com"
    )
    
    # Configuration emails
    email_signature = models.TextField(
        blank=True,
        default="Cordialement,\nL'équipe Zsdevweb"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprise"
    
    def __str__(self):
        return self.name
    
    @classmethod
    def get_instance(cls):
        """Récupère ou crée l'instance unique"""
        instance, created = cls.objects.get_or_create(id=1)
        return instance


class ProjectType(models.Model):
    """Types de projets (Site vitrine, E-commerce, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estimated_days = models.IntegerField(default=10, help_text="Nombre de jours estimés")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Type de projet"
        verbose_name_plural = "Types de projets"

    def __str__(self):
        return self.name


class DesignOption(models.Model):
    """Options de design (Simple, Moderne, Premium)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price_supplement = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['price_supplement']
        verbose_name = "Option de design"
        verbose_name_plural = "Options de design"

    def __str__(self):
        return self.name


class ComplexityLevel(models.Model):
    """Niveaux de complexité (Basique, Intermédiaire, Avancé)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price_multiplier = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['price_multiplier']
        verbose_name = "Niveau de complexité"
        verbose_name_plural = "Niveaux de complexité"

    def __str__(self):
        return self.name


class SupplementaryOption(models.Model):
    """Options supplémentaires (SEO, Maintenance, etc.)"""
    BILLING_TYPE_CHOICES = [
        ('one_time', 'Paiement unique'),
        ('monthly', 'Mensuel'),
        ('yearly', 'Annuel'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    billing_type = models.CharField(max_length=20, choices=BILLING_TYPE_CHOICES, default='one_time')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Option supplémentaire"
        verbose_name_plural = "Options supplémentaires"

    def __str__(self):
        return f"{self.name} ({self.get_billing_type_display()})"


class QuoteTemplate(models.Model):
    """Templates de devis réutilisables"""
    name = models.CharField(max_length=200, unique=True, verbose_name="Nom du template")
    description = models.TextField(blank=True)
    
    # Configuration par défaut
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    design_option = models.ForeignKey(DesignOption, on_delete=models.CASCADE)
    complexity_level = models.ForeignKey(ComplexityLevel, on_delete=models.CASCADE)
    supplementary_options = models.ManyToManyField(SupplementaryOption, blank=True)
    
    # Texte par défaut
    default_description = models.TextField(
        verbose_name="Description par défaut",
        help_text="Texte prérempli pour ce type de projet"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Template de devis"
        verbose_name_plural = "Templates de devis"
    
    def __str__(self):
        return self.name


class Quote(models.Model):
    """Devis créés par les utilisateurs"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('sent', 'Envoyé'),
        ('viewed', 'Consulté'),
        ('accepted', 'Accepté'),
        ('rejected', 'Refusé'),
        ('expired', 'Expiré'),
    ]

    # Informations client
    client_name = models.CharField(max_length=200, verbose_name="Nom du client")
    client_email = models.EmailField(verbose_name="Email du client")
    client_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    company_name = models.CharField(max_length=200, blank=True, verbose_name="Nom de l'entreprise")
    client_address = models.TextField(blank=True, verbose_name="Adresse")

    # Configuration du projet
    project_type = models.ForeignKey(ProjectType, on_delete=models.PROTECT, verbose_name="Type de projet")
    design_option = models.ForeignKey(DesignOption, on_delete=models.PROTECT, verbose_name="Option de design")
    complexity_level = models.ForeignKey(ComplexityLevel, on_delete=models.PROTECT, verbose_name="Niveau de complexité")
    supplementary_options = models.ManyToManyField(SupplementaryOption, blank=True, verbose_name="Options supplémentaires")

    # Template utilisé (optionnel)
    template = models.ForeignKey(
        QuoteTemplate, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Créé depuis le template"
    )

    # Détails du projet
    project_description = models.TextField(verbose_name="Description du projet")
    deadline = models.DateField(null=True, blank=True, verbose_name="Date limite souhaitée")

    # Calculs financiers
    subtotal_ht = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Sous-total HT",
        default=0
    )
    
    # Système de remise
    discount_type = models.CharField(
        max_length=10,
        choices=[('percent', 'Pourcentage'), ('fixed', 'Montant fixe')],
        blank=True,
        verbose_name="Type de remise"
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Valeur de la remise"
    )
    discount_reason = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Raison de la remise",
        help_text="Ex: Client fidèle, Promotion, etc."
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Montant de la remise"
    )
    
    tva_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('20.00'),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Taux TVA (%)"
    )
    tva_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Montant TVA",
        default=0
    )
    total_ttc = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Total TTC",
        default=0
    )

    # Conditions de paiement
    payment_first = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="1er paiement (30%)",
        default=0
    )
    payment_second = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="2ème paiement (40%)",
        default=0
    )
    payment_final = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Paiement final (30%)",
        default=0
    )

    # Durée estimée
    estimated_duration_days = models.IntegerField(
        default=0,
        verbose_name="Durée estimée (jours)"
    )
    estimated_start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de début estimée"
    )
    estimated_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin estimée"
    )
    
    # PDF du devis
    pdf_file = models.FileField(
        upload_to='quotes/pdf/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Fichier PDF"
    )
    
    # Signature électronique
    signature_token = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="Token de signature"
    )
    signature_image = models.ImageField(
        upload_to='quotes/signatures/',
        blank=True,
        null=True,
        verbose_name="Image de la signature"
    )
    signed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Signé le"
    )
    client_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP du client"
    )
    
    # Statut et suivi
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")
    quote_number = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Numéro de devis")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Expire le")
    
    # Notes internes (invisible au client)
    internal_notes = models.TextField(
        blank=True,
        verbose_name="Notes internes",
        help_text="Visible uniquement par les admins"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_quotes',
        verbose_name="Assigné à"
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Envoyé le")
    viewed_at = models.DateTimeField(null=True, blank=True, verbose_name="Consulté le")
    accepted_at = models.DateTimeField(null=True, blank=True, verbose_name="Accepté le")
    rejected_at = models.DateTimeField(null=True, blank=True, verbose_name="Refusé le")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Devis"
        verbose_name_plural = "Devis"

    def __str__(self):
        return f"Devis #{self.quote_number or self.id} - {self.client_name}"
    
    # ========== MÉTHODE MODIFIÉE ========== #
    def calculate_prices(self, skip_m2m=False):
        """
        Calcule tous les prix du devis avec remise

        Args:
            skip_m2m: Si True, ignore les relations ManyToMany (pour la création initiale)
        """
        # 1. Prix de base
        subtotal = Decimal('0.00')

        if self.project_type:
            subtotal = self.project_type.base_price

        # 2. Option de design
        if self.design_option:
            subtotal += self.design_option.price_supplement

        # 3. Multiplicateur de complexité
        if self.complexity_level:
            subtotal *= self.complexity_level.price_multiplier

        # 4. Options supplémentaires (paiement unique uniquement)
        # Ne pas accéder aux M2M si l'objet n'a pas encore d'ID
        if not skip_m2m and self.pk:
            for option in self.supplementary_options.filter(billing_type='one_time'):
                subtotal += option.price

        # 5. Calcul de la remise
        discount_amount = Decimal('0.00')
        if self.discount_value > 0:
            if self.discount_type == 'percent':
                discount_amount = subtotal * (self.discount_value / Decimal('100'))
            elif self.discount_type == 'fixed':
                discount_amount = self.discount_value

        # 6. Sous-total après remise
        subtotal_after_discount = subtotal - discount_amount

        # 7. TVA
        tva_amount = subtotal_after_discount * (self.tva_rate / Decimal('100'))

        # 8. Total TTC
        total_ttc = subtotal_after_discount + tva_amount

        # 9. Répartition des paiements (30% / 40% / 30%)
        payment_first = total_ttc * Decimal('0.30')
        payment_second = total_ttc * Decimal('0.40')
        payment_final = total_ttc * Decimal('0.30')

        # 10. Durée estimée
        estimated_days = self.project_type.estimated_days if self.project_type else 10
        if self.complexity_level:
            estimated_days = int(estimated_days * float(self.complexity_level.price_multiplier))

        return {
            'subtotal_ht': round(subtotal, 2),
            'discount_amount': round(discount_amount, 2),
            'subtotal_after_discount': round(subtotal_after_discount, 2),
            'tva_amount': round(tva_amount, 2),
            'total_ttc': round(total_ttc, 2),
            'payment_first': round(payment_first, 2),
            'payment_second': round(payment_second, 2),
            'payment_final': round(payment_final, 2),
            'estimated_duration_days': estimated_days,
        }
    
    def generate_quote_number(self):
        """Génère un numéro de devis unique : DEVIS-YYYYMM-XXX"""
        if not self.quote_number:
            date_part = timezone.now().strftime('%Y%m')
            count = Quote.objects.filter(
                quote_number__startswith=f'DEVIS-{date_part}'
            ).count() + 1
            self.quote_number = f'DEVIS-{date_part}-{count:03d}'
    
    def generate_signature_token(self):
        """Génère un token unique pour la signature électronique"""
        if not self.signature_token:
            alphabet = string.ascii_letters + string.digits
            self.signature_token = ''.join(secrets.choice(alphabet) for _ in range(64))
    
    def calculate_expiration_date(self):
        """Calcule la date d'expiration (30 jours après création)"""
        if not self.expires_at:
            from datetime import timedelta
            self.expires_at = timezone.now() + timedelta(days=30)
    
    def check_if_expired(self):
        """Vérifie et marque le devis comme expiré si nécessaire"""
        if self.expires_at and timezone.now() > self.expires_at and self.status in ['draft', 'sent', 'viewed']:
            self.status = 'expired'
            self.save(update_fields=['status'])
            return True
        return False
    
    @property
    def is_expired(self):
        """Vérifie si le devis est expiré"""
        return self.expires_at and timezone.now() > self.expires_at
    
    @property
    def signature_url(self):
        """URL de signature électronique"""
        if self.signature_token:
            return f"/devis/sign/{self.signature_token}/"
        return None
    
    # ========== MÉTHODE MODIFIÉE ========== #
    def save(self, *args, **kwargs):
        """Calcule automatiquement les prix avant la sauvegarde"""
        # Vérifier si c'est une création (pas d'ID)
        is_new = self.pk is None

        # Générer le numéro de devis
        if not self.quote_number:
            self.generate_quote_number()

        # Générer le token de signature
        if not self.signature_token:
            self.generate_signature_token()

        # Calculer la date d'expiration
        if not self.expires_at:
            self.calculate_expiration_date()

        # Calculer les prix (skip M2M si création)
        prices = self.calculate_prices(skip_m2m=is_new)
        self.subtotal_ht = prices['subtotal_ht']
        self.discount_amount = prices['discount_amount']
        self.tva_amount = prices['tva_amount']
        self.total_ttc = prices['total_ttc']
        self.payment_first = prices['payment_first']
        self.payment_second = prices['payment_second']
        self.payment_final = prices['payment_final']
        self.estimated_duration_days = prices['estimated_duration_days']

        # Calculer les dates estimées
        if self.estimated_start_date and not self.estimated_end_date:
            from datetime import timedelta
            self.estimated_end_date = self.estimated_start_date + timedelta(days=self.estimated_duration_days)

        super().save(*args, **kwargs)

        # Si c'était une création et qu'il y a des options supplémentaires à ajouter,
        # recalculer les prix après que les M2M soient sauvegardées
        # Cela sera géré par le serializer/view


class QuoteEmailLog(models.Model):
    """Log des emails envoyés pour les devis"""
    EMAIL_TYPE_CHOICES = [
        ('created', 'Création du devis'),
        ('reminder', 'Rappel'),
        ('accepted', 'Acceptation'),
        ('rejected', 'Refus'),
    ]
    
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='email_logs')
    email_type = models.CharField(max_length=20, choices=EMAIL_TYPE_CHOICES)
    recipient = models.EmailField()
    subject = models.CharField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Log d'email"
        verbose_name_plural = "Logs d'emails"
    
    def __str__(self):
        return f"{self.get_email_type_display()} - {self.recipient} - {self.sent_at.strftime('%d/%m/%Y')}"