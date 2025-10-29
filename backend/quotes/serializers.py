"""
Serializers pour l'API Quotes Premium
"""
from rest_framework import serializers
from django.utils import timezone
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


class CompanySerializer(serializers.ModelSerializer):
    """Serializer pour les informations de l'entreprise"""
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'logo', 'email', 'phone', 'address',
            'siret', 'tva_number', 'primary_color', 'footer_text',
            'email_signature', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProjectTypeSerializer(serializers.ModelSerializer):
    """Serializer pour les types de projets"""
    
    class Meta:
        model = ProjectType
        fields = '__all__'


class DesignOptionSerializer(serializers.ModelSerializer):
    """Serializer pour les options de design"""
    
    class Meta:
        model = DesignOption
        fields = '__all__'


class ComplexityLevelSerializer(serializers.ModelSerializer):
    """Serializer pour les niveaux de complexité"""
    
    class Meta:
        model = ComplexityLevel
        fields = '__all__'


class SupplementaryOptionSerializer(serializers.ModelSerializer):
    """Serializer pour les options supplémentaires"""
    
    billing_type_display = serializers.CharField(source='get_billing_type_display', read_only=True)
    
    class Meta:
        model = SupplementaryOption
        fields = '__all__'


class QuoteTemplateSerializer(serializers.ModelSerializer):
    """Serializer pour les templates de devis"""
    
    project_type_detail = ProjectTypeSerializer(source='project_type', read_only=True)
    design_option_detail = DesignOptionSerializer(source='design_option', read_only=True)
    complexity_level_detail = ComplexityLevelSerializer(source='complexity_level', read_only=True)
    supplementary_options_detail = SupplementaryOptionSerializer(source='supplementary_options', many=True, read_only=True)
    
    class Meta:
        model = QuoteTemplate
        fields = [
            'id', 'name', 'description',
            'project_type', 'project_type_detail',
            'design_option', 'design_option_detail',
            'complexity_level', 'complexity_level_detail',
            'supplementary_options', 'supplementary_options_detail',
            'default_description', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuoteListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des devis"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    project_type_name = serializers.CharField(source='project_type.name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Quote
        fields = [
            'id', 'quote_number', 'client_name', 'client_email',
            'company_name', 'project_type_name', 'status', 'status_display',
            'total_ttc', 'is_expired', 'created_at', 'expires_at'
        ]


class QuoteDetailSerializer(serializers.ModelSerializer):
    """Serializer complet pour un devis"""
    
    # Relations en détail
    project_type_detail = ProjectTypeSerializer(source='project_type', read_only=True)
    design_option_detail = DesignOptionSerializer(source='design_option', read_only=True)
    complexity_level_detail = ComplexityLevelSerializer(source='complexity_level', read_only=True)
    supplementary_options_detail = SupplementaryOptionSerializer(source='supplementary_options', many=True, read_only=True)
    
    # Champs calculés
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    discount_type_display = serializers.CharField(source='get_discount_type_display', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    signature_url = serializers.CharField(read_only=True)
    
    class Meta:
        model = Quote
        fields = [
            # Identifiants
            'id', 'quote_number',
            
            # Client
            'client_name', 'client_email', 'client_phone',
            'company_name', 'client_address',
            
            # Configuration
            'project_type', 'project_type_detail',
            'design_option', 'design_option_detail',
            'complexity_level', 'complexity_level_detail',
            'supplementary_options', 'supplementary_options_detail',
            'template',
            
            # Détails projet
            'project_description', 'deadline',
            
            # Financier
            'subtotal_ht', 'discount_type', 'discount_type_display',
            'discount_value', 'discount_reason', 'discount_amount',
            'tva_rate', 'tva_amount', 'total_ttc',
            
            # Paiements
            'payment_first', 'payment_second', 'payment_final',
            
            # Planning
            'estimated_duration_days', 'estimated_start_date', 'estimated_end_date',
            
            # PDF
            'pdf_file',
            
            # Signature
            'signature_token', 'signature_url', 'signature_image',
            'signed_at', 'client_ip',
            
            # Statut
            'status', 'status_display', 'expires_at', 'is_expired',
            
            # Notes internes (visible uniquement par staff)
            'internal_notes', 'assigned_to',
            
            # Dates
            'created_at', 'updated_at', 'sent_at', 'viewed_at',
            'accepted_at', 'rejected_at'
        ]
        read_only_fields = [
            'id', 'quote_number', 'subtotal_ht', 'discount_amount',
            'tva_amount', 'total_ttc', 'payment_first', 'payment_second',
            'payment_final', 'estimated_duration_days', 'signature_token',
            'signature_url', 'is_expired', 'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        """Masquer les notes internes pour les non-staff"""
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        # Si l'utilisateur n'est pas staff, masquer les notes internes
        if request and not (request.user and request.user.is_staff):
            data.pop('internal_notes', None)
            data.pop('assigned_to', None)
        
        return data


class QuoteCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création de devis"""
    
    class Meta:
        model = Quote
        fields = [
            'client_name', 'client_email', 'client_phone',
            'company_name', 'client_address',
            'project_type', 'design_option', 'complexity_level',
            'supplementary_options', 'template',
            'project_description', 'deadline',
            'discount_type', 'discount_value', 'discount_reason',
            'tva_rate', 'estimated_start_date'
        ]
    
    def validate_client_email(self, value):
        """Validation de l'email"""
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Format d'email invalide")
        return value.lower()
    
    def validate_discount_value(self, value):
        """Validation de la remise"""
        if value < 0:
            raise serializers.ValidationError("La remise ne peut pas être négative")
        if value > 100 and self.initial_data.get('discount_type') == 'percent':
            raise serializers.ValidationError("La remise ne peut pas dépasser 100%")
        return value


class QuoteEmailLogSerializer(serializers.ModelSerializer):
    """Serializer pour les logs d'emails"""
    
    email_type_display = serializers.CharField(source='get_email_type_display', read_only=True)
    
    class Meta:
        model = QuoteEmailLog
        fields = '__all__'
        read_only_fields = ['id', 'sent_at']


class QuoteStatisticsSerializer(serializers.Serializer):
    """Serializer pour les statistiques des devis"""
    
    total_quotes = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    status_breakdown = serializers.DictField()
    conversion_rate = serializers.FloatField()
    
    quotes_by_month = serializers.ListField()
    top_project_types = serializers.ListField()