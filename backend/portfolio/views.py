from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .models import Technology, Project, Testimonial
from .serializers import (
    TechnologySerializer, ProjectListSerializer, ProjectDetailSerializer,
    TestimonialSerializer
)


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les technologies"""
    queryset = Technology.objects.filter(is_active=True)
    serializer_class = TechnologySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['name', 'category']
    ordering = ['category', 'name']


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les projets - optimisé avec prefetch_related"""
    queryset = Project.objects.filter(is_published=True).prefetch_related('technologies')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['featured']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'completion_date', 'created_at']
    ordering = ['order', '-completion_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectDetailSerializer


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les témoignages"""
    queryset = Testimonial.objects.filter(is_published=True)
    serializer_class = TestimonialSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating', 'project']
    ordering_fields = ['order', 'created_at', 'rating']
    ordering = ['order', '-created_at']


@api_view(['GET'])
@permission_classes([AllowAny])
def statistics(request):
    """
    Endpoint pour récupérer les statistiques du portfolio

    Returns:
        - total_projects: Nombre total de projets réalisés
        - total_clients: Nombre de clients satisfaits (basé sur les témoignages)
        - satisfaction_rate: Taux de satisfaction moyen (basé sur les ratings des témoignages)
        - years_experience: Années d'expérience
    """
    # Compter les projets publiés
    total_projects = Project.objects.filter(is_published=True).count()

    # Compter les clients uniques (témoignages avec clients différents)
    unique_clients = Testimonial.objects.filter(is_published=True).values('client_name').distinct().count()

    # Calculer le taux de satisfaction moyen (basé sur les ratings /5)
    avg_rating = Testimonial.objects.filter(is_published=True).aggregate(
        avg=Avg('rating')
    )['avg'] or 0

    # Convertir la note moyenne sur 5 en pourcentage
    satisfaction_rate = round((avg_rating / 5.0) * 100, 1) if avg_rating > 0 else 100

    # Années d'expérience (peut être configuré ou calculé depuis la date du premier projet)
    years_experience = 5  # Valeur par défaut

    # Si on a des projets avec dates de complétion, calculer depuis le plus ancien
    from django.utils import timezone
    oldest_project = Project.objects.filter(
        is_published=True,
        completion_date__isnull=False
    ).order_by('completion_date').first()

    if oldest_project and oldest_project.completion_date:
        years_diff = (timezone.now().date() - oldest_project.completion_date).days / 365.25
        if years_diff > 0:
            years_experience = max(int(years_diff), 1)

    return Response({
        'total_projects': total_projects,
        'total_clients': unique_clients,
        'satisfaction_rate': satisfaction_rate,
        'years_experience': years_experience,
    })