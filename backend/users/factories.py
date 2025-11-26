"""
Factories pour générer des données de test pour l'app users
"""
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory pour créer des utilisateurs de test"""
    
    class Meta:
        model = User
        django_get_or_create = ('username',)
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    
    user_type = 'client'
    phone = '+33612345678'
    company_name = factory.Faker('company')
    email_notifications = True
    is_active = True


class AdminUserFactory(UserFactory):
    """Factory pour créer des utilisateurs admin"""
    
    user_type = 'admin'
    is_staff = True
    is_superuser = False


class SuperUserFactory(UserFactory):
    """Factory pour créer des super utilisateurs"""
    
    user_type = 'admin'
    is_staff = True
    is_superuser = True