from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ProjectType(models.Model):
    """Types de projets (Site vitrine, E-commerce, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
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
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Option supplémentaire"
        verbose_name_plural = "Options supplémentaires"

    def __str__(self):
        return self.name


class Quote(models.Model):
    """Devis créés par les utilisateurs"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('sent', 'Envoyé'),
        ('accepted', 'Accepté'),
        ('rejected', 'Refusé'),
    ]

    # Informations client
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200, blank=True)

    # Configuration du projet
    project_type = models.ForeignKey(ProjectType, on_delete=models.PROTECT)
    design_option = models.ForeignKey(DesignOption, on_delete=models.PROTECT)
    complexity_level = models.ForeignKey(ComplexityLevel, on_delete=models.PROTECT)
    supplementary_options = models.ManyToManyField(SupplementaryOption, blank=True)

    # Détails du projet
    project_description = models.TextField()
    deadline = models.DateField(null=True, blank=True)

    # Prix
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Devis"
        verbose_name_plural = "Devis"

    def __str__(self):
        return f"Devis #{self.id} - {self.client_name}"
    
    def calculate_total_price(self):
        """Calcule le prix total du devis"""
        total = 0
        
        if self.project_type:
            total = self.project_type.base_price
        
        if self.design_option:
            total += self.design_option.price_supplement
        
        if self.complexity_level:
            total *= self.complexity_level.price_multiplier
        
        # Ajouter les options supplémentaires
        for option in self.supplementary_options.all():
            total += option.price
        
        return total
    
    def save(self, *args, **kwargs):
        """Calcule automatiquement le prix total avant la sauvegarde"""
        # Ne calculer le prix que lors des mises à jour (pas lors de la création)
        # et seulement si ce n'est pas explicitement mis à jour
        if self.pk and 'update_fields' not in kwargs:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

# Create your models here.
