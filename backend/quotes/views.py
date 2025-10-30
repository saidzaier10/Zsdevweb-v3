from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Q, Count, Sum
from decimal import Decimal

from .models import (
    Company,
    ProjectType,
    DesignOption,
    Feature,
    ComplexityLevel,
    SupplementaryOption,
    Quote
)
from .serializers import (
    CompanySerializer,
    ProjectTypeSerializer,
    DesignOptionSerializer,
    FeatureSerializer,
    ComplexityLevelSerializer,
    SupplementaryOptionSerializer,
    QuoteSerializer,
    QuoteCreateSerializer,
    QuoteDetailSerializer
)
from .permissions import IsAdminOrReadOnly
from .pdf_generator import generate_quote_pdf
from .emails import (
    send_quote_created_email,
    send_quote_accepted_email,
    send_quote_rejected_email
)


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les types d'entreprises.
    Lecture seule pour tout le monde.
    """
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]


class ProjectTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les types de projets.
    Lecture seule pour tout le monde.
    """
    queryset = ProjectType.objects.filter(is_active=True)
    serializer_class = ProjectTypeSerializer
    permission_classes = [AllowAny]


class DesignOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les options de design.
    Lecture seule pour tout le monde.
    """
    queryset = DesignOption.objects.filter(is_active=True)
    serializer_class = DesignOptionSerializer
    permission_classes = [AllowAny]


class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les fonctionnalités.
    Lecture seule pour tout le monde.
    """
    queryset = Feature.objects.filter(is_active=True)
    serializer_class = FeatureSerializer
    permission_classes = [AllowAny]


class ComplexityLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les niveaux de complexité.
    Lecture seule pour tout le monde.
    """
    queryset = ComplexityLevel.objects.filter(is_active=True)
    serializer_class = ComplexityLevelSerializer
    permission_classes = [AllowAny]


class SupplementaryOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les options supplémentaires.
    Lecture seule pour tout le monde.
    """
    queryset = SupplementaryOption.objects.filter(is_active=True)
    serializer_class = SupplementaryOptionSerializer
    permission_classes = [AllowAny]


class QuoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les devis.
    - Tout le monde peut créer un devis (POST)
    - Seuls les admins peuvent lister/modifier/supprimer
    - Actions publiques : public (GET par token), sign (POST signature)
    """
    queryset = Quote.objects.all().select_related(
        'company',
        'project_type',
        'complexity_level'
    ).prefetch_related(
        'design_options',
        'features',
        'supplementary_options'
    )
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'company', 'project_type']
    search_fields = ['quote_number', 'client_name', 'client_email', 'client_company']
    ordering_fields = ['created_at', 'valid_until', 'total_ttc']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Utilise des serializers différents selon l'action"""
        if self.action == 'create':
            return QuoteCreateSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return QuoteDetailSerializer
        return QuoteSerializer

    def get_permissions(self):
        """Permissions personnalisées selon l'action"""
        if self.action in ['create', 'public', 'sign']:
            return [AllowAny()]
        elif self.action == 'my_quotes':
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Créer un nouveau devis et envoyer l'email"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quote = serializer.save()
        
        # Envoyer l'email de création
        send_quote_created_email(quote)
        
        # Retourner la réponse avec le serializer détaillé
        response_serializer = QuoteDetailSerializer(quote)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='download-pdf')
    def download_pdf(self, request, pk=None):
        """Télécharger le PDF du devis"""
        quote = self.get_object()
        
        try:
            pdf_buffer = generate_quote_pdf(quote)
            
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{quote.quote_number}.pdf"'
            
            return response
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la génération du PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], url_path='send-email')
    def send_email(self, request, pk=None):
        """Envoyer l'email du devis au client"""
        quote = self.get_object()
        
        # Envoyer l'email
        success = send_quote_created_email(quote)
        
        if success:
            # Mettre à jour le statut si c'était un brouillon
            if quote.status == 'draft':
                quote.status = 'sent'
                quote.save(update_fields=['status'])
            
            return Response({'message': 'Email envoyé avec succès'})
        else:
            return Response(
                {'error': 'Erreur lors de l\'envoi de l\'email'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='public/(?P<token>[^/.]+)')
    def public(self, request, token=None):
        """Récupérer un devis via son token public (sans authentification)"""
        quote = get_object_or_404(Quote, public_token=token)
        
        # Mettre à jour le statut à 'viewed' si c'était 'sent'
        if quote.status == 'sent':
            quote.status = 'viewed'
            quote.save(update_fields=['status'])
        
        serializer = QuoteDetailSerializer(quote)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='sign/(?P<token>[^/.]+)')
    def sign_quote(self, request, token=None):
        """Signer un devis via son token public"""
        quote = get_object_or_404(Quote, public_token=token)
        
        # Vérifier que le devis n'est pas déjà signé
        if quote.status == 'accepted':
            return Response(
                {'error': 'Ce devis a déjà été signé'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier que le devis n'est pas expiré
        if quote.valid_until and quote.valid_until < timezone.now().date():
            quote.status = 'expired'
            quote.save(update_fields=['status'])
            return Response(
                {'error': 'Ce devis a expiré'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer les données de signature
        signature_name = request.data.get('signature_name')
        signature_image = request.data.get('signature_image')
        
        if not signature_name or not signature_image:
            return Response(
                {'error': 'Le nom et la signature sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour le devis
        quote.status = 'accepted'
        quote.signature_name = signature_name
        quote.signature_image = signature_image
        quote.signed_at = timezone.now()
        quote.ip_address = self.get_client_ip(request)
        quote.save()
        
        # Envoyer l'email de confirmation
        send_quote_accepted_email(quote)
        
        serializer = QuoteDetailSerializer(quote)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Dupliquer un devis existant"""
        original_quote = self.get_object()
        
        # Créer une copie
        quote_copy = Quote.objects.get(pk=original_quote.pk)
        quote_copy.pk = None
        quote_copy.quote_number = None  # Sera généré automatiquement
        quote_copy.status = 'draft'
        quote_copy.signature_name = None
        quote_copy.signature_image = None
        quote_copy.signed_at = None
        quote_copy.ip_address = None
        quote_copy.save()
        
        # Copier les relations ManyToMany
        quote_copy.design_options.set(original_quote.design_options.all())
        quote_copy.features.set(original_quote.features.all())
        quote_copy.supplementary_options.set(original_quote.supplementary_options.all())
        
        serializer = QuoteDetailSerializer(quote_copy)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='my-quotes')
    def my_quotes(self, request):
        """Récupérer les devis de l'utilisateur connecté par email"""
        user_email = request.user.email
        
        queryset = self.get_queryset().filter(client_email=user_email)
        
        # Filtrer par statut si demandé
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtenir les statistiques sur les devis"""
        from django.db.models import Count, Sum, Q
        
        queryset = self.get_queryset()
        
        stats = {
            'total_quotes': queryset.count(),
            'draft_quotes': queryset.filter(status='draft').count(),
            'sent_quotes': queryset.filter(status='sent').count(),
            'viewed_quotes': queryset.filter(status='viewed').count(),
            'accepted_quotes': queryset.filter(status='accepted').count(),
            'rejected_quotes': queryset.filter(status='rejected').count(),
            'expired_quotes': queryset.filter(status='expired').count(),
            'pending_quotes': queryset.filter(status__in=['sent', 'viewed']).count(),
            'total_revenue': queryset.filter(status='accepted').aggregate(
                total=Sum('total_ttc')
            )['total'] or Decimal('0.00'),
        }
        
        return Response(stats)

    def get_client_ip(self, request):
        """Obtenir l'adresse IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip