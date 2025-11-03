from django.db import models
from django.core.validators import URLValidator


class Technology(models.Model):
    """Technologies utilisées (Python, Django, Vue.js, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Nom de l'icône (ex: devicon-python-plain)")
    category = models.CharField(max_length=50, choices=[
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Base de données'),
        ('devops', 'DevOps'),
        ('other', 'Autre'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = "Technologie"
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name


class Project(models.Model):
    """Projets du portfolio"""

    CATEGORY_CHOICES = [
        ('web', 'Site Web'),
        ('ecommerce', 'E-commerce'),
        ('mobile', 'Application Mobile'),
        ('api', 'API / Backend'),
        ('other', 'Autre'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web', help_text="Catégorie du projet")

    # Images
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', blank=True, null=True)
    image_main = models.ImageField(upload_to='projects/main/', blank=True, null=True)

    # Technologies
    technologies = models.ManyToManyField(Technology, related_name='projects')

    # Liens
    github_url = models.URLField(blank=True, validators=[URLValidator()])
    live_url = models.URLField(blank=True, validators=[URLValidator()])

    # Métadonnées
    featured = models.BooleanField(default=False, help_text="Projet mis en avant sur la page d'accueil")
    order = models.IntegerField(default=0, help_text="Ordre d'affichage (0 = premier)")
    is_published = models.BooleanField(default=True)
    
    # Dates
    completion_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-completion_date']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published', 'featured']),
            models.Index(fields=['is_published', 'order']),
        ]
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    """Images supplémentaires pour un projet"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Image de projet"
        verbose_name_plural = "Images de projets"

    def __str__(self):
        return f"{self.project.title} - Image {self.order}"


class Testimonial(models.Model):
    """Témoignages clients"""
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=200, blank=True)
    client_company = models.CharField(max_length=200, blank=True)
    client_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    
    content = models.TextField()
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

    def __str__(self):
        return f"{self.client_name} - {self.rating}★"

# Create your models here.
