"""
Views pour l'API Quotes Premium
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from django.http import FileResponse
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from .models import (
    Company,
    ProjectType,
    DesignOption,
    ComplexityLevel,
    SupplementaryOption,
    QuoteTemplate,
    Quote,
    QuoteEmailLog
)
from .serializers import (
    CompanySerializer,
    ProjectTypeSerializer,
    DesignOptionSerializer,
    ComplexityLevelSerializer,
    SupplementaryOptionSerializer,
    QuoteTemplateSerializer,
    QuoteListSerializer,
    QuoteDetailSerializer,
    QuoteCreateSerializer,
    QuoteEmailLogSerializer,
    QuoteStatisticsSerializer
)
from .permissions import IsAdminOrReadOnly
from .pdf_generator import QuotePDFGenerator
from .emails import (
    send_quote_created_email,
    send_quote_accepted_email,
    send_quote_reminder_email
)

logger = logging.getLogger('quotes')


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les informations de l'entreprise
    GET: Accessible à tous
    POST/PUT/PATCH/DELETE: Admin uniquement
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProjectTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour les types de projets
    Filtre automatiquement pour ne montrer que les types actifs
    """
    serializer_class = ProjectTypeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ProjectType.objects.filter(is_active=True)


class DesignOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour les options de design
    Filtre automatiquement pour ne montrer que les options actives
    """
    serializer_class = DesignOptionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return DesignOption.objects.filter(is_active=True)


class ComplexityLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour les niveaux de complexité
    Filtre automatiquement pour ne montrer que les niveaux actifs
    """
    serializer_class = ComplexityLevelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ComplexityLevel.objects.filter(is_active=True)


class SupplementaryOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour les options supplémentaires
    Supporte le filtrage par type de facturation
    """
    serializer_class = SupplementaryOptionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = SupplementaryOption.objects.filter(is_active=True)
        
        # Filtrage par type de facturation
        billing_type = self.request.query_params.get('billing_type')
        if billing_type:
            queryset = queryset.filter(billing_type=billing_type)
        
        return queryset


class QuoteTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour les templates de devis
    Les admins voient tous les templates, les autres uniquement les actifs
    """
    serializer_class = QuoteTemplateSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return QuoteTemplate.objects.all()
        return QuoteTemplate.objects.filter(is_active=True)


class QuoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet principal pour la gestion des devis
    - POST (create): Accessible à tous (création publique)
    - GET (list): Admin uniquement
    - GET (retrieve): Admin ou avec token
    - PUT/PATCH/DELETE: Admin uniquement
    """
    queryset = Quote.objects.all().select_related(
        'project_type', 'design_option', 'complexity_level'
    ).prefetch_related('supplementary_options')

    def get_permissions(self):
        """Définir les permissions selon l'action"""
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['list', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['my_quotes']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        """Choisir le serializer selon l'action"""
        if self.action == 'list':
            return QuoteListSerializer
        elif self.action == 'create':
            return QuoteCreateSerializer
        return QuoteDetailSerializer

    def get_queryset(self):
        """Filtrer les devis selon les paramètres"""
        queryset = super().get_queryset()
        
        # Filtrage par statut
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """Créer un nouveau devis et envoyer l'email"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quote = serializer.save()
        
        # Envoyer l'email de création
        send_quote_created_email(quote)
        
        logger.info(
            f"Nouveau devis créé: #{quote.quote_number} pour {quote.client_name}",
            extra={'quote_id': quote.id}
        )
        
        # Retourner le devis complet
        detail_serializer = QuoteDetailSerializer(quote, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_quotes(self, request):
        """Liste des devis de l'utilisateur connecté (par email)"""
        email = request.user.email
        
        if not email:
            return Response(
                {'error': 'Email utilisateur non trouvé'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer les devis de cet email
        quotes = Quote.objects.filter(client_email=email).order_by('-created_at')
        
        # Filtrage optionnel par statut
        status_filter = request.query_params.get('status')
        if status_filter:
            quotes = quotes.filter(status=status_filter)
        
        # Pagination
        page = self.paginate_queryset(quotes)
        if page is not None:
            serializer = QuoteListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = QuoteListSerializer(quotes, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Télécharger le PDF du devis"""
        quote = self.get_object()
        
        try:
            # Générer le PDF
            generator = QuotePDFGenerator(quote)
            pdf_buffer = generator.generate()
            
            # Retourner le PDF
            response = FileResponse(
                pdf_buffer,
                content_type='application/pdf',
                as_attachment=True,
                filename=f'devis_{quote.quote_number}.pdf'
            )
            
            logger.info(
                f"PDF téléchargé pour le devis #{quote.quote_number}",
                extra={'quote_id': quote.id}
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"Erreur génération PDF pour devis #{quote.quote_number}: {str(e)}",
                extra={'quote_id': quote.id}
            )
            return Response(
                {'error': 'Erreur lors de la génération du PDF'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def send_email(self, request, pk=None):
        """Envoyer le devis par email au client"""
        quote = self.get_object()
        
        # Envoyer l'email
        success = send_quote_created_email(quote)
        
        if success:
            # Mettre à jour le statut si c'était un brouillon
            if quote.status == 'draft':
                quote.status = 'sent'
                quote.sent_at = timezone.now()
                quote.save(update_fields=['status', 'sent_at'])
            
            logger.info(
                f"Email envoyé pour le devis #{quote.quote_number}",
                extra={'quote_id': quote.id}
            )
            
            return Response({
                'message': 'Email envoyé avec succès',
                'sent_at': quote.sent_at
            })
        else:
            return Response(
                {'error': "Erreur lors de l'envoi de l'email"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='public/(?P<token>[^/.]+)')
    def public_view(self, request, token=None):
        """Vue publique d'un devis via son token (sans authentification)"""
        try:
            quote = Quote.objects.get(signature_token=token)
        except Quote.DoesNotExist:
            return Response(
                {'error': 'Devis non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Marquer comme consulté si c'est la première fois
        if quote.status == 'sent' and not quote.viewed_at:
            quote.status = 'viewed'
            quote.viewed_at = timezone.now()
            quote.save(update_fields=['status', 'viewed_at'])
            
            logger.info(
                f"Devis #{quote.quote_number} consulté pour la première fois",
                extra={'quote_id': quote.id}
            )
        
        serializer = QuoteDetailSerializer(quote, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='sign/(?P<token>[^/.]+)')
    def sign_quote(self, request, token=None):
        """Signer un devis électroniquement (sans authentification)"""
        try:
            quote = Quote.objects.get(signature_token=token)
        except Quote.DoesNotExist:
            return Response(
                {'error': 'Devis non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier que le devis n'est pas déjà signé
        if quote.status == 'accepted':
            return Response(
                {'error': 'Ce devis a déjà été signé'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier que le devis n'est pas expiré
        if quote.is_expired:
            return Response(
                {'error': 'Ce devis a expiré'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer les données de signature
        signature_data = request.data.get('signature_data')
        client_name = request.data.get('client_name')
        
        if not signature_data or not client_name:
            return Response(
                {'error': 'Données de signature manquantes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Sauvegarder la signature
        # TODO: Implémenter le stockage de l'image de signature
        quote.status = 'accepted'
        quote.signed_at = timezone.now()
        quote.accepted_at = timezone.now()
        quote.client_ip = self._get_client_ip(request)
        quote.save(update_fields=['status', 'signed_at', 'accepted_at', 'client_ip'])
        
        # Envoyer l'email de confirmation
        send_quote_accepted_email(quote)
        
        logger.info(
            f"Devis #{quote.quote_number} signé par {client_name}",
            extra={'quote_id': quote.id, 'ip': quote.client_ip}
        )
        
        serializer = QuoteDetailSerializer(quote, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """Statistiques globales des devis (admin uniquement)"""
        # Stats basiques
        total_quotes = Quote.objects.count()
        total_amount = Quote.objects.aggregate(total=Sum('total_ttc'))['total'] or Decimal('0.00')
        average_amount = Quote.objects.aggregate(avg=Avg('total_ttc'))['avg'] or Decimal('0.00')
        
        # Répartition par statut
        status_breakdown = {}
        for status_choice in Quote.STATUS_CHOICES:
            status_key = status_choice[0]
            count = Quote.objects.filter(status=status_key).count()
            status_breakdown[status_key] = count
        
        # Taux de conversion (acceptés / envoyés)
        sent_count = Quote.objects.filter(status__in=['sent', 'viewed', 'accepted']).count()
        accepted_count = Quote.objects.filter(status='accepted').count()
        conversion_rate = (accepted_count / sent_count * 100) if sent_count > 0 else 0
        
        # Devis par mois (12 derniers mois)
        quotes_by_month = []
        now = timezone.now()
        for i in range(12):
            month_start = (now - timedelta(days=30*i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            count = Quote.objects.filter(
                created_at__gte=month_start,
                created_at__lte=month_end
            ).count()
            quotes_by_month.append({
                'month': month_start.strftime('%Y-%m'),
                'count': count
            })
        quotes_by_month.reverse()
        
        # Top types de projets
        top_project_types = Quote.objects.values(
            'project_type__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        data = {
            'total_quotes': total_quotes,
            'total_amount': total_amount,
            'average_amount': average_amount,
            'status_breakdown': status_breakdown,
            'conversion_rate': round(conversion_rate, 2),
            'quotes_by_month': quotes_by_month,
            'top_project_types': list(top_project_types)
        }
        
        serializer = QuoteStatisticsSerializer(data)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def duplicate(self, request, pk=None):
        """Dupliquer un devis (admin uniquement)"""
        original_quote = self.get_object()
        
        # Créer une copie
        new_quote = Quote.objects.create(
            client_name=original_quote.client_name,
            client_email=original_quote.client_email,
            client_phone=original_quote.client_phone,
            company_name=original_quote.company_name,
            client_address=original_quote.client_address,
            project_type=original_quote.project_type,
            design_option=original_quote.design_option,
            complexity_level=original_quote.complexity_level,
            project_description=original_quote.project_description,
            deadline=original_quote.deadline,
            discount_type=original_quote.discount_type,
            discount_value=original_quote.discount_value,
            discount_reason=original_quote.discount_reason,
            tva_rate=original_quote.tva_rate,
            estimated_start_date=original_quote.estimated_start_date,
            status='draft'
        )
        
        # Copier les options supplémentaires
        new_quote.supplementary_options.set(original_quote.supplementary_options.all())
        
        logger.info(
            f"Devis #{original_quote.quote_number} dupliqué en #{new_quote.quote_number}",
            extra={'original_id': original_quote.id, 'new_id': new_quote.id}
        )
        
        serializer = QuoteDetailSerializer(new_quote, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_client_ip(self, request):
        """Récupérer l'IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class QuoteEmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour les logs d'emails
    Admin uniquement
    Supporte le filtrage par devis
    """
    serializer_class = QuoteEmailLogSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = QuoteEmailLog.objects.all()
        
        # Filtrage par devis
        quote_id = self.request.query_params.get('quote')
        if quote_id:
            queryset = queryset.filter(quote_id=quote_id)
        
        return queryset.order_by('-sent_at')