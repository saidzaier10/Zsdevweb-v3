"""
API Views pour les devis - Version complète avec emails
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from datetime import timedelta

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
from .pdf_generator import QuotePDFGenerator
from .emails import (
    send_quote_created_email,
    send_quote_accepted_email,
    send_quote_rejected_email
)


class CompanyViewSet(viewsets.ModelViewSet):
    """API pour gérer les informations de l'entreprise"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        """Seuls les admins peuvent créer/modifier/supprimer"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ProjectTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour récupérer les types de projets"""
    queryset = ProjectType.objects.filter(is_active=True)
    serializer_class = ProjectTypeSerializer
    permission_classes = [permissions.AllowAny]


class DesignOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour récupérer les options de design"""
    queryset = DesignOption.objects.filter(is_active=True)
    serializer_class = DesignOptionSerializer
    permission_classes = [permissions.AllowAny]


class ComplexityLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour récupérer les niveaux de complexité"""
    queryset = ComplexityLevel.objects.filter(is_active=True)
    serializer_class = ComplexityLevelSerializer
    permission_classes = [permissions.AllowAny]


class SupplementaryOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour récupérer les options supplémentaires"""
    queryset = SupplementaryOption.objects.filter(is_active=True)
    serializer_class = SupplementaryOptionSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Filtrer par type de facturation"""
        queryset = super().get_queryset()
        billing_type = self.request.query_params.get('billing_type', None)
        if billing_type:
            queryset = queryset.filter(billing_type=billing_type)
        return queryset


class QuoteTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour récupérer les templates de devis"""
    queryset = QuoteTemplate.objects.filter(is_active=True)
    serializer_class = QuoteTemplateSerializer
    
    def get_permissions(self):
        """Admins uniquement pour modification"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        """Admins voient tout, autres voient seulement actifs"""
        if self.request.user and self.request.user.is_staff:
            return QuoteTemplate.objects.all()
        return QuoteTemplate.objects.filter(is_active=True)


class QuoteViewSet(viewsets.ModelViewSet):
    """API pour gérer les devis"""
    queryset = Quote.objects.all().select_related(
        'project_type',
        'design_option',
        'complexity_level',
        'template'
    ).prefetch_related('supplementary_options')
    
    def get_serializer_class(self):
        """Choisir le serializer selon l'action"""
        if self.action == 'list':
            return QuoteListSerializer
        elif self.action == 'create':
            return QuoteCreateSerializer
        return QuoteDetailSerializer
    
    def get_permissions(self):
        """Permissions par action"""
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action in ['list', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        """Admins voient tout, autres ne voient rien (ils utilisent my_quotes)"""
        queryset = super().get_queryset()
        
        if self.request.user and self.request.user.is_staff:
            status_filter = self.request.query_params.get('status', None)
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            return queryset
        
        return queryset.none()
    
    def create(self, request, *args, **kwargs):
        """Créer un devis, générer le PDF et envoyer l'email"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quote = serializer.save()

        # Générer le PDF automatiquement
        try:
            from django.core.files.base import ContentFile

            generator = QuotePDFGenerator(quote)
            pdf_buffer = generator.generate()
            pdf_content = pdf_buffer.getvalue()

            # Sauvegarder le PDF dans le modèle
            quote.pdf_file.save(
                f'devis_{quote.quote_number}.pdf',
                ContentFile(pdf_content),
                save=True
            )
            print(f"✅ PDF généré avec succès: devis_{quote.quote_number}.pdf")
        except Exception as e:
            print(f"❌ Erreur génération PDF: {e}")
            # On continue même si la génération du PDF échoue

        # Envoyer l'email de création avec le PDF en pièce jointe
        try:
            send_quote_created_email(quote)
            quote.status = 'sent'
            quote.sent_at = timezone.now()
            quote.save(update_fields=['status', 'sent_at'])
        except Exception as e:
            print(f"Erreur envoi email: {e}")

        detail_serializer = QuoteDetailSerializer(quote, context={'request': request})

        return Response(
            detail_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_quotes(self, request):
        """Récupère les devis créés par l'utilisateur connecté

        GET /api/quotes/my-quotes/
        GET /api/quotes/my-quotes/?status=sent
        """
        # CHANGEMENT : Filtre par created_by au lieu de client_email
        queryset = Quote.objects.filter(
            created_by=request.user
        ).select_related(
            'project_type',
            'design_option',
            'complexity_level'
        ).prefetch_related('supplementary_options').order_by('-created_at')

        # Filtrer par statut si demandé
        status_filter = request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        serializer = QuoteListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='download-pdf')
    def download_pdf(self, request, pk=None):
        """Télécharger le PDF du devis"""
        quote = self.get_object()
        
        generator = QuotePDFGenerator(quote)
        pdf_buffer = generator.generate()
        
        from django.core.files.base import ContentFile
        pdf_content = pdf_buffer.getvalue()
        quote.pdf_file.save(
            f'devis_{quote.quote_number}.pdf',
            ContentFile(pdf_content),
            save=True
        )
        
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="devis_{quote.quote_number}.pdf"'
        return response
    
    @action(detail=True, methods=['post'], url_path='send-email')
    def send_email(self, request, pk=None):
        """Envoyer le devis par email"""
        quote = self.get_object()
        
        try:
            send_quote_created_email(quote)
            quote.status = 'sent'
            quote.sent_at = timezone.now()
            quote.save(update_fields=['status', 'sent_at'])
            
            return Response({
                'message': 'Email envoyé avec succès',
                'sent_at': quote.sent_at
            })
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de l\'envoi: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='public/(?P<token>[^/.]+)', permission_classes=[permissions.AllowAny])
    def public_view(self, request, token=None):
        """Voir un devis avec le token public (sans authentification)"""
        quote = get_object_or_404(Quote, signature_token=token)
        
        if not quote.viewed_at:
            quote.viewed_at = timezone.now()
            if quote.status == 'sent':
                quote.status = 'viewed'
            quote.save()
        
        serializer = QuoteDetailSerializer(quote, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='sign/(?P<token>[^/.]+)', permission_classes=[permissions.AllowAny])
    def sign_quote(self, request, token=None):
        """Signer électroniquement un devis"""
        quote = get_object_or_404(Quote, signature_token=token)
        
        if quote.signed_at:
            return Response(
                {'error': 'Ce devis a déjà été signé'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if quote.is_expired:
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
        
        quote.signature_image = signature_data
        quote.signer_name = signer_name
        quote.signed_at = timezone.now()
        quote.accepted_at = timezone.now()
        quote.status = 'accepted'
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            quote.client_ip = x_forwarded_for.split(',')[0]
        else:
            quote.client_ip = request.META.get('REMOTE_ADDR')
        
        quote.save()
        
        try:
            send_quote_accepted_email(quote)
        except Exception as e:
            print(f"Erreur envoi email acceptation: {e}")
        
        serializer = QuoteDetailSerializer(quote, context={'request': request})
        return Response({
            'message': 'Devis signé avec succès',
            'quote': serializer.data
        })
    
    @action(detail=True, methods=['post'], url_path='reject')
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
        quote.rejected_at = timezone.now()
        quote.save()
        
        try:
            send_quote_rejected_email(quote)
        except Exception as e:
            print(f"Erreur envoi email refus: {e}")
        
        serializer = QuoteDetailSerializer(quote, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='statistics', permission_classes=[permissions.IsAdminUser])
    def statistics(self, request):
        """Statistiques des devis (admin uniquement)"""
        total_quotes = Quote.objects.count()
        
        aggregates = Quote.objects.aggregate(
            total_amount=Sum('total_ttc'),
            average_amount=Avg('total_ttc')
        )
        
        status_breakdown = dict(
            Quote.objects.values('status').annotate(count=Count('id')).values_list('status', 'count')
        )
        
        sent_count = Quote.objects.filter(status__in=['sent', 'viewed', 'accepted']).count()
        accepted_count = Quote.objects.filter(status='accepted').count()
        conversion_rate = (accepted_count / sent_count * 100) if sent_count > 0 else 0
        
        twelve_months_ago = timezone.now() - timedelta(days=365)
        quotes_by_month = Quote.objects.filter(
            created_at__gte=twelve_months_ago
        ).extra(
            select={'month': "TO_CHAR(created_at, 'YYYY-MM')"}
        ).values('month').annotate(
            count=Count('id'),
            total=Sum('total_ttc')
        ).order_by('month')
        
        top_project_types = Quote.objects.values(
            'project_type__name'
        ).annotate(
            count=Count('id'),
            total_amount=Sum('total_ttc')
        ).order_by('-count')[:5]
        
        stats_data = {
            'total_quotes': total_quotes,
            'total_amount': aggregates['total_amount'] or 0,
            'average_amount': aggregates['average_amount'] or 0,
            'status_breakdown': status_breakdown,
            'conversion_rate': round(conversion_rate, 2),
            'quotes_by_month': list(quotes_by_month),
            'top_project_types': list(top_project_types)
        }
        
        serializer = QuoteStatisticsSerializer(stats_data)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='duplicate')
    def duplicate(self, request, pk=None):
        """Dupliquer un devis"""
        original_quote = self.get_object()
        
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
        
        new_quote.supplementary_options.set(original_quote.supplementary_options.all())
        
        prices = new_quote.calculate_prices(skip_m2m=False)
        for field, value in prices.items():
            setattr(new_quote, field, value)
        new_quote.save()
        
        serializer = QuoteDetailSerializer(new_quote, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuoteEmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour consulter les logs d'emails"""
    queryset = QuoteEmailLog.objects.all()
    serializer_class = QuoteEmailLogSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        """Filtrer par devis si spécifié"""
        queryset = super().get_queryset()
        quote_id = self.request.query_params.get('quote', None)
        if quote_id:
            queryset = queryset.filter(quote_id=quote_id)
        return queryset