from rest_framework import serializers
from django.core.validators import EmailValidator, MinValueValidator
from django.core.exceptions import ValidationError
import bleach
import re
from datetime import date, timedelta

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
        read_only_fields = ['total_price', 'created_at', 'updated_at', 'status']
        extra_kwargs = {
            'client_name': {
                'required': True,
                'min_length': 2,
                'max_length': 200
            },
            'client_email': {
                'required': True,
                'validators': [EmailValidator(message="Adresse email invalide")]
            },
            'client_phone': {
                'required': False,
                'allow_blank': True,
                'max_length': 20
            },
            'company_name': {
                'required': False,
                'allow_blank': True,
                'max_length': 200
            },
            'project_description': {
                'required': True,
                'min_length': 10,
                'max_length': 5000
            },
            'project_type': {'required': True},
            'design_option': {'required': True},
            'complexity_level': {'required': True},
        }
    
    def validate_client_name(self, value):
        """Validation et nettoyage du nom client"""
        # Nettoyer les tags HTML
        value = bleach.clean(value, tags=[], strip=True).strip()
        
        if not value:
            raise serializers.ValidationError("Le nom du client ne peut pas être vide")
        
        if len(value) < 2:
            raise serializers.ValidationError("Le nom du client doit contenir au moins 2 caractères")
        
        if len(value) > 200:
            raise serializers.ValidationError("Le nom du client ne peut pas dépasser 200 caractères")
        
        # Vérifier qu'il contient au moins quelques caractères alphabétiques
        if not re.search(r'[a-zA-ZÀ-ÿ]', value):
            raise serializers.ValidationError("Le nom du client doit contenir des lettres")
        
        return value
    
    def validate_client_email(self, value):
        """Validation stricte de l'email"""
        # Nettoyer et normaliser
        value = bleach.clean(value, tags=[], strip=True).strip().lower()
        
        if not value:
            raise serializers.ValidationError("L'email ne peut pas être vide")
        
        # Vérifier le format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Format d'email invalide")
        
        # Vérifier la longueur totale
        if len(value) > 254:  # RFC 5321
            raise serializers.ValidationError("L'email est trop long")
        
        # Vérifier que le domaine n'est pas suspect
        suspicious_domains = ['tempmail.com', 'throwaway.email', '10minutemail.com', 'guerrillamail.com']
        domain = value.split('@')[1] if '@' in value else ''
        if domain in suspicious_domains:
            raise serializers.ValidationError("Ce domaine email n'est pas autorisé")
        
        return value
    
    def validate_client_phone(self, value):
        """Validation du téléphone"""
        if not value:
            return ''
        
        # Nettoyer
        value = bleach.clean(value, tags=[], strip=True).strip()
        
        # Supprimer les espaces, tirets, parenthèses
        cleaned = re.sub(r'[\s\-\(\)]', '', value)
        
        # Vérifier le format
        phone_regex = r'^\+?1?\d{9,15}$'
        if not re.match(phone_regex, cleaned):
            raise serializers.ValidationError("Format de téléphone invalide (utilisez le format international, ex: +33612345678)")
        
        return cleaned
    
    def validate_company_name(self, value):
        """Validation du nom de l'entreprise"""
        if not value:
            return ''
        
        # Nettoyer
        value = bleach.clean(value, tags=[], strip=True).strip()
        
        if len(value) > 200:
            raise serializers.ValidationError("Le nom de l'entreprise ne peut pas dépasser 200 caractères")
        
        return value
    
    def validate_project_description(self, value):
        """Validation de la description du projet"""
        # Nettoyer les tags HTML mais garder les retours à la ligne
        value = bleach.clean(value, tags=[], strip=True).strip()
        
        if not value:
            raise serializers.ValidationError("La description du projet ne peut pas être vide")
        
        if len(value) < 10:
            raise serializers.ValidationError("La description doit contenir au moins 10 caractères")
        
        if len(value) > 5000:
            raise serializers.ValidationError("La description ne peut pas dépasser 5000 caractères")
        
        # Vérifier qu'il y a du contenu significatif (pas que des espaces/ponctuation)
        meaningful_chars = re.sub(r'[\s\.,;:!?]', '', value)
        if len(meaningful_chars) < 5:
            raise serializers.ValidationError("La description doit contenir du texte significatif")
        
        return value
    
    def validate_deadline(self, value):
        """Validation de la date limite"""
        if not value:
            return None
        
        # Vérifier que la date n'est pas dans le passé
        if value < date.today():
            raise serializers.ValidationError("La date limite ne peut pas être dans le passé")
        
        # Vérifier que la date n'est pas trop loin dans le futur (ex: 2 ans max)
        max_future_date = date.today() + timedelta(days=730)  # 2 ans
        if value > max_future_date:
            raise serializers.ValidationError("La date limite ne peut pas être dans plus de 2 ans")
        
        return value
    
    def validate_project_type(self, value):
        """Vérifier que le type de projet existe et est actif"""
        if not value:
            raise serializers.ValidationError("Le type de projet est requis")
        
        if not value.is_active:
            raise serializers.ValidationError("Ce type de projet n'est plus disponible")
        
        return value
    
    def validate_design_option(self, value):
        """Vérifier que l'option de design existe et est active"""
        if not value:
            raise serializers.ValidationError("L'option de design est requise")
        
        if not value.is_active:
            raise serializers.ValidationError("Cette option de design n'est plus disponible")
        
        return value
    
    def validate_complexity_level(self, value):
        """Vérifier que le niveau de complexité existe et est actif"""
        if not value:
            raise serializers.ValidationError("Le niveau de complexité est requis")
        
        if not value.is_active:
            raise serializers.ValidationError("Ce niveau de complexité n'est plus disponible")
        
        return value
    
    def validate_supplementary_options(self, value):
        """Vérifier que toutes les options supplémentaires sont actives"""
        if not value:
            return []
        
        # Limiter le nombre d'options supplémentaires
        if len(value) > 10:
            raise serializers.ValidationError("Vous ne pouvez pas sélectionner plus de 10 options supplémentaires")
        
        # Vérifier que toutes les options sont actives
        for option in value:
            if not option.is_active:
                raise serializers.ValidationError(f"L'option '{option.name}' n'est plus disponible")
        
        return value
    
    def validate(self, attrs):
        """Validation globale du devis"""
        # Vérifier la cohérence des données
        project_type = attrs.get('project_type')
        design_option = attrs.get('design_option')
        complexity_level = attrs.get('complexity_level')
        
        if project_type and design_option and complexity_level:
            # Calculer le prix estimé pour vérifier la cohérence
            estimated_price = (project_type.base_price + design_option.price_supplement) * complexity_level.price_multiplier
            
            # Ajouter les options supplémentaires
            supp_options = attrs.get('supplementary_options', [])
            for option in supp_options:
                estimated_price += option.price
            
            # Vérifier que le prix n'est pas anormalement élevé (protection contre manipulation)
            if estimated_price > 1000000:  # 1 million d'euros
                raise serializers.ValidationError("Le montant du devis semble anormalement élevé")
        
        return attrs
    
    def create(self, validated_data):
        """Créer un devis avec calcul automatique du prix"""
        # Récupérer les options supplémentaires
        supplementary_options = validated_data.pop('supplementary_options', [])
        
        # Initialiser le prix à 0
        validated_data['total_price'] = 0
        
        # Créer le devis
        quote = Quote.objects.create(**validated_data)
        
        # Ajouter les options supplémentaires
        if supplementary_options:
            quote.supplementary_options.set(supplementary_options)
        
        # Calculer et sauvegarder le prix final
        quote.total_price = quote.calculate_total_price()
        quote.save(update_fields=['total_price'])
        
        return quote
    
    def update(self, instance, validated_data):
        """Mise à jour d'un devis avec recalcul du prix"""
        # Récupérer les options supplémentaires
        supplementary_options = validated_data.pop('supplementary_options', None)
        
        # Mettre à jour les champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Mettre à jour les options supplémentaires si fournies
        if supplementary_options is not None:
            instance.supplementary_options.set(supplementary_options)
        
        # Recalculer le prix
        instance.total_price = instance.calculate_total_price()
        instance.save()
        
        return instance