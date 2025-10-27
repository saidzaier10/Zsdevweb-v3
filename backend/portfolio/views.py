from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
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
    """API endpoint pour les projets"""
    queryset = Project.objects.filter(is_published=True)
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