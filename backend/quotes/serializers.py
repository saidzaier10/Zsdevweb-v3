from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Sum
from django.http import HttpResponse

from .models import (
    Company,
    ProjectType,
    DesignOption,
    ComplexityLevel,
    SupplementaryOption,
    Quote
)
from .serializers import (
    CompanySerializer,
    ProjectTypeSerializer,
    DesignOptionSerializer,
    ComplexityLevelSerializer,
    SupplementaryOptionSerializer,
    QuoteListSerializer,
    QuoteDetailSerializer,
    QuoteCreateSerializer
)
from .permissions import IsAdminOrReadOnly
from .emails import send_quote_created_email, send_quote_accepted_email, send_quote_rejected_email


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProjectTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectType.objects.filter(is_active=True)
    serializer_class = ProjectTypeSerializer
    permission_classes = [permissions.AllowAny]


class DesignOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DesignOption.objects.filter(is_active=True)
    serializer_class = DesignOptionSerializer
    permission_classes = [permissions.AllowAny]


class ComplexityLevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ComplexityLevel.objects.filter(is_active=True)
    serializer_class = ComplexityLevelSerializer
    permission_classes = [permissions.AllowAny]


class SupplementaryOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SupplementaryOption.objects.filter(is_active=True)
    serializer_class = SupplementaryOptionSerializer
    permission_classes = [permissions.AllowAny]


class QuoteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Quote.objects.select_related(
            'company',
            'project_type',
            'design_option',
            'complexity_level'
        ).prefetch_related('supplementary_options')
        
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            return queryset.all()
        return queryset.filter(company__user=user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return QuoteCreateSerializer
        elif self.action == 'retrieve':
            return QuoteDetailSerializer
        return QuoteListSerializer
    
    def perform_create(self, serializer):
        quote = serializer.save()
        send_quote_created_email(quote)
    
    @action(detail=False, methods=['get'])
    def my_quotes(self, request):
        """Récupère les devis de l'utilisateur connecté"""
        queryset = self.get_queryset().filter(company__user=request.user)
        
        status_filter = request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        queryset = queryset.order_by('-created_at')
        
        serializer = QuoteListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def statistics(self, request):
        """Statistiques pour l'admin"""
        total_quotes = Quote.objects.count()
        accepted_quotes = Quote.objects.filter(status='accepted').count()
        pending_quotes = Quote.objects.filter(status__in=['sent', 'viewed']).count()
        
        total_revenue = Quote.objects.filter(status='accepted').aggregate(
            total=Sum('total_price_with_tax')
        )['total'] or 0
        
        recent_quotes = Quote.objects.select_related(
            'company'
        ).order_by('-created_at')[:10]
        
        return Response({
            'total_quotes': total_quotes,
            'accepted_quotes': accepted_quotes,
            'pending_quotes': pending_quotes,
            'total_revenue': float(total_revenue),
            'recent_quotes': QuoteListSerializer(recent_quotes, many=True).data
        })
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplique un devis existant"""
        original_quote = self.get_object()
        
        new_quote = Quote.objects.create(
            company=original_quote.company,
            project_type=original_quote.project_type,
            design_option=original_quote.design_option,
            complexity_level=original_quote.complexity_level,
            estimated_pages=original_quote.estimated_pages,
            custom_features=original_quote.custom_features,
            notes=original_quote.notes,
            validity_days=original_quote.validity_days,
            status='draft'
        )
        
        new_quote.supplementary_options.set(original_quote.supplementary_options.all())
        
        prices = new_quote.calculate_prices(skip_m2m=False)
        for field, value in prices.items():
            setattr(new_quote, field, value)
        new_quote.save()
        
        serializer = QuoteDetailSerializer(new_quote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Télécharge le PDF du devis"""
        quote = self.get_object()
        
        try:
            pdf_content = quote.generate_pdf()
            
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="devis_{quote.quote_number}.pdf"'
            
            return response
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la génération du PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='sign/(?P<token>[^/.]+)', permission_classes=[permissions.AllowAny])
    def sign_quote(self, request, token=None):
        """Signature électronique du devis via token"""
        try:
            quote = Quote.objects.get(signature_token=token)
        except Quote.DoesNotExist:
            return Response(
                {'error': 'Token invalide ou devis introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if quote.status == 'accepted':
            return Response(
                {'error': 'Ce devis a déjà été signé'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if quote.is_expired():
            return Response(
                {'error': 'Ce devis a expiré'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        signature_data = request.data.get('signature')
        signer_name = request.data.get('signer_name')
        terms_accepted = request.data.get('terms_accepted', False)
        
        if not signature_data or not signer_name or not terms_accepted:
            return Response(
                {'error': 'Données de signature incomplètes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        quote.client_signature = signature_data
        quote.signer_name = signer_name
        quote.signed_at = timezone.now()
        quote.status = 'accepted'
        quote.save()
        
        send_quote_accepted_email(quote)
        
        serializer = QuoteDetailSerializer(quote)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='public/(?P<token>[^/.]+)', permission_classes=[permissions.AllowAny])
    def public_detail(self, request, token=None):
        """Récupère un devis via token pour signature publique"""
        try:
            quote = Quote.objects.select_related(
                'company',
                'project_type',
                'design_option',
                'complexity_level'
            ).prefetch_related('supplementary_options').get(signature_token=token)
            
            if quote.status != 'sent' or not quote.is_valid():
                quote.status = 'viewed'
                quote.save()
            
            serializer = QuoteDetailSerializer(quote)
            return Response(serializer.data)
        except Quote.DoesNotExist:
            return Response(
                {'error': 'Token invalide ou devis introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Rejeter un devis"""
        quote = self.get_object()
        
        if quote.status == 'accepted':
            return Response(
                {'error': 'Un devis accepté ne peut pas être rejeté'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rejection_reason = request.data.get('reason', '')
        
        quote.status = 'rejected'
        quote.rejection_reason = rejection_reason
        quote.save()
        
        send_quote_rejected_email(quote)
        
        serializer = QuoteDetailSerializer(quote)
        return Response(serializer.data)