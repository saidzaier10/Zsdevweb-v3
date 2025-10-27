from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ProjectType, DesignOption, ComplexityLevel, SupplementaryOption, Quote
from .serializers import (
    ProjectTypeSerializer, DesignOptionSerializer, ComplexityLevelSerializer,
    SupplementaryOptionSerializer, QuoteSerializer
)


class ProjectTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les types de projets"""
    queryset = ProjectType.objects.filter(is_active=True)
    serializer_class = ProjectTypeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'base_price']
    ordering = ['name']


class DesignOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les options de design"""
    queryset = DesignOption.objects.filter(is_active=True)
    serializer_class = DesignOptionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price_supplement']
    ordering = ['price_supplement']


class ComplexityLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les niveaux de complexité"""
    queryset = ComplexityLevel.objects.filter(is_active=True)
    serializer_class = ComplexityLevelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price_multiplier']
    ordering = ['price_multiplier']


class SupplementaryOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les options supplémentaires"""
    queryset = SupplementaryOption.objects.filter(is_active=True)
    serializer_class = SupplementaryOptionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price']
    ordering = ['name']


class QuoteViewSet(viewsets.ModelViewSet):
    """API endpoint pour les devis"""
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'project_type', 'design_option', 'complexity_level']
    search_fields = ['client_name', 'client_email', 'company_name', 'project_description']
    ordering_fields = ['created_at', 'total_price']
    ordering = ['-created_at']

# Create your views here.
