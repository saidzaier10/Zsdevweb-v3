from rest_framework import serializers
from .models import ProjectType, DesignOption, ComplexityLevel, SupplementaryOption, Quote


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ['id', 'name', 'description', 'base_price', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class DesignOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignOption
        fields = ['id', 'name', 'description', 'price_supplement', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ComplexityLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexityLevel
        fields = ['id', 'name', 'description', 'price_multiplier', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class SupplementaryOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplementaryOption
        fields = ['id', 'name', 'description', 'price', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class QuoteSerializer(serializers.ModelSerializer):
    project_type_details = ProjectTypeSerializer(source='project_type', read_only=True)
    design_option_details = DesignOptionSerializer(source='design_option', read_only=True)
    complexity_level_details = ComplexityLevelSerializer(source='complexity_level', read_only=True)
    supplementary_options_details = SupplementaryOptionSerializer(source='supplementary_options', many=True, read_only=True)
    
    class Meta:
        model = Quote
        fields = [
            'id', 'client_name', 'client_email', 'client_phone', 'company_name',
            'project_type', 'project_type_details',
            'design_option', 'design_option_details',
            'complexity_level', 'complexity_level_details',
            'supplementary_options', 'supplementary_options_details',
            'project_description', 'deadline', 'total_price', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['total_price', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Récupérer les options supplémentaires
        supplementary_options = validated_data.pop('supplementary_options', [])
        
        # Créer le devis sans le sauvegarder encore
        quote = Quote(**validated_data)
        
        # Initialiser le prix à 0 pour éviter NULL
        quote.total_price = 0
        quote.save()
        
        # Ajouter les options supplémentaires
        if supplementary_options:
            quote.supplementary_options.set(supplementary_options)
        
        # Recalculer et sauvegarder le prix final
        quote.total_price = quote.calculate_total_price()
        quote.save()
        
        return quote