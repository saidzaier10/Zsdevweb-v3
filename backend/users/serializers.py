from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'phone', 'company_name']
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        # Récupérer les options supplémentaires
        supplementary_options = validated_data.pop('supplementary_options', [])
        
        # Initialiser total_price à 0 pour éviter les problèmes lors de la création
        validated_data['total_price'] = 0
        
        # Créer le devis sans calculer le prix
        quote = Quote.objects.create(**validated_data)
        
        # Ajouter les options supplémentaires (maintenant que l'objet a un ID)
        if supplementary_options:
            quote.supplementary_options.set(supplementary_options)
        
        # Maintenant calculer et sauvegarder le prix total
        quote.total_price = quote.calculate_total_price()
        quote.save(update_fields=['total_price'])  # Ne sauvegarde que le champ total_price
        
        return quote

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'company_name', 'user_type', 'avatar']
        read_only_fields = ['id', 'user_type']

class CustomTokenObtainPairSerializer(serializers.Serializer):
    """Serializer pour la connexion avec username/password"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError('Identifiants incorrects.')
        
        if not user.is_active:
            raise serializers.ValidationError('Compte désactivé.')
        
        # Générer les tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }