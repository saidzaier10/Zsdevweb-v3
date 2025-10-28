from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import bleach
import logging

from .models import ProjectType, DesignOption, ComplexityLevel, SupplementaryOption, Quote
from .serializers import (
    ProjectTypeSerializer, DesignOptionSerializer, ComplexityLevelSerializer,
    SupplementaryOptionSerializer, QuoteSerializer
)
from .permissions import IsAdminOrCreateOnly

logger = logging.getLogger('quotes')


class QuoteCreationRateThrottle(AnonRateThrottle):
    """Rate limiting pour la création de devis"""
    rate = '5/hour'


class ProjectTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les types de projets"""
    queryset = ProjectType.objects.filter(is_active=True)
    serializer_class = ProjectTypeSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'base_price']
    ordering = ['name']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class DesignOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les options de design"""
    queryset = DesignOption.objects.filter(is_active=True)
    serializer_class = DesignOptionSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price_supplement']
    ordering = ['price_supplement']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class ComplexityLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les niveaux de complexité"""
    queryset = ComplexityLevel.objects.filter(is_active=True)
    serializer_class = ComplexityLevelSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price_multiplier']
    ordering = ['price_multiplier']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class SupplementaryOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint pour les options supplémentaires"""
    queryset = SupplementaryOption.objects.filter(is_active=True)
    serializer_class = SupplementaryOptionSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price']
    ordering = ['name']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class QuoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les devis
    
    - POST: Tout le monde peut créer un devis (rate limited)
    - GET/PUT/DELETE: Seuls les admins peuvent accéder aux devis existants
    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [IsAdminOrCreateOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'project_type', 'design_option', 'complexity_level']
    search_fields = ['client_name', 'client_email', 'company_name', 'project_description']
    ordering_fields = ['created_at', 'total_price']
    ordering = ['-created_at']
    
    def get_throttles(self):
        """Appliquer un rate limiting strict sur la création de devis"""
        if self.action == 'create':
            return [QuoteCreationRateThrottle()]
        return [UserRateThrottle()]
    
    def create(self, request, *args, **kwargs):
        """Créer un devis avec validation et sanitization"""
        logger.info(f"Nouvelle demande de devis depuis IP: {self.get_client_ip(request)}")
        
        # Sanitize les données textuelles pour éviter les XSS
        sanitized_data = self.sanitize_quote_data(request.data.copy())
        
        # Valider l'email
        email = sanitized_data.get('client_email', '')
        try:
            validate_email(email)
        except ValidationError:
            logger.warning(f"Email invalide dans demande de devis: {email}")
            return Response(
                {"client_email": ["Adresse email invalide"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valider la longueur de la description
        description = sanitized_data.get('project_description', '')
        if len(description) < 10:
            return Response(
                {"project_description": ["La description doit contenir au moins 10 caractères"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(description) > 5000:
            return Response(
                {"project_description": ["La description ne peut pas dépasser 5000 caractères"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer le devis
        serializer = self.get_serializer(data=sanitized_data)
        serializer.is_valid(raise_exception=True)
        quote = serializer.save()
        
        logger.info(f"Devis créé avec succès - ID: {quote.id}, Email: {quote.client_email}, Total: {quote.total_price}€")
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Mise à jour d'un devis (admin uniquement)"""
        quote = self.get_object()
        logger.info(f"Mise à jour du devis #{quote.id} par {request.user.username}")
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Suppression d'un devis (admin uniquement)"""
        quote = self.get_object()
        logger.warning(f"Suppression du devis #{quote.id} par {request.user.username}")
        return super().destroy(request, *args, **kwargs)
    
    def sanitize_quote_data(self, data):
        """Nettoie les données pour éviter les injections XSS"""
        text_fields = ['client_name', 'client_email', 'client_phone', 'company_name', 'project_description']
        
        for field in text_fields:
            if field in data and isinstance(data[field], str):
                # Supprimer les tags HTML et scripts
                data[field] = bleach.clean(
                    data[field],
                    tags=[],  # Aucun tag HTML autorisé
                    strip=True
                )
                # Limiter la longueur
                if field == 'project_description':
                    data[field] = data[field][:5000]
                else:
                    data[field] = data[field][:200]
        
        return data
    
    def get_client_ip(self, request):
        """Récupère l'IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """Obtenir des statistiques sur les devis (admin uniquement)"""
        from django.db.models import Count, Sum, Avg
        
        stats = {
            'total_quotes': Quote.objects.count(),
            'by_status': dict(Quote.objects.values('status').annotate(count=Count('id')).values_list('status', 'count')),
            'total_revenue': Quote.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0,
            'average_price': Quote.objects.aggregate(Avg('total_price'))['total_price__avg'] or 0,
        }
        
        logger.info(f"Statistiques consultées par {request.user.username}")
        
        return Response(stats)