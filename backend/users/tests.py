"""
Tests unitaires pour l'app users
"""
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import UserFactory, AdminUserFactory
import unittest.mock

User = get_user_model()


# ============================================================
# TESTS DES MODÈLES
# ============================================================

class UserModelTestCase(TestCase):
    """Tests pour le modèle User"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.user = UserFactory(username='testuser')
        self.admin = AdminUserFactory(username='adminuser')
    
    def test_user_creation(self):
        """Test la création d'un utilisateur"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.user_type, 'client')
        self.assertTrue(self.user.email_notifications)
    
    def test_user_str_representation(self):
        """Test la représentation string d'un utilisateur"""
        expected = f"{self.user.username} (Client)"
        self.assertEqual(str(self.user), expected)
    
    def test_is_client_property(self):
        """Test la propriété is_client"""
        self.assertTrue(self.user.is_client)
        self.assertFalse(self.admin.is_client)
    
    def test_is_admin_user_property(self):
        """Test la propriété is_admin_user"""
        self.assertFalse(self.user.is_admin_user)
        self.assertTrue(self.admin.is_admin_user)
    
    def test_user_timestamps(self):
        """Test que les timestamps sont créés automatiquement"""
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)
    
    def test_user_ordering(self):
        """Test l'ordre par défaut des utilisateurs"""
        user1 = UserFactory(username='user1')
        user2 = UserFactory(username='user2')
        users = User.objects.all()
        # Le plus récent doit être en premier
        self.assertEqual(users[0].username, 'user2')


# ============================================================
# TESTS DES API ENDPOINTS
# ============================================================

@override_settings(WAF_BLOCK_MODE=False, REST_FRAMEWORK={'DEFAULT_THROTTLE_CLASSES': [], 'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication']})
class UserRegistrationAPITestCase(APITestCase):
    """Tests pour l'endpoint d'inscription"""
    
    def setUp(self):
        """Configuration initiale"""
        self.client = APIClient()
        self.url = '/api/auth/register/'
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password2': 'securepass123',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        
        # Disable throttling
        from users.views import RegisterRateThrottle
        self.throttle_patcher = unittest.mock.patch.object(RegisterRateThrottle, 'allow_request', return_value=True)
        self.throttle_patcher.start()
        self.addCleanup(self.throttle_patcher.stop)
    
    def test_register_user_success(self):
        """Test l'inscription réussie d'un utilisateur"""
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        
        # Vérifier que l'utilisateur existe en base
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.user_type, 'client')  # Par défaut
    
    def test_register_password_mismatch(self):
        """Test l'inscription avec des mots de passe différents"""
        data = self.valid_data.copy()
        data['password2'] = 'differentpass'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_duplicate_username(self):
        """Test l'inscription avec un username déjà existant"""
        UserFactory(username='newuser')
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_invalid_email(self):
        """Test l'inscription avec un email invalide"""
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_missing_fields(self):
        """Test l'inscription avec des champs manquants"""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(WAF_BLOCK_MODE=False, REST_FRAMEWORK={'DEFAULT_THROTTLE_CLASSES': [], 'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication']})
class UserLoginAPITestCase(APITestCase):
    """Tests pour l'endpoint de connexion"""
    
    def setUp(self):
        """Configuration initiale"""
        self.client = APIClient()
        self.url = '/api/auth/login/'
        self.user = UserFactory(username='testuser')
        # Le password est défini à 'testpass123' dans la factory
        
        # Disable throttling
        from users.views import LoginRateThrottle
        self.throttle_patcher = unittest.mock.patch.object(LoginRateThrottle, 'allow_request', return_value=True)
        self.throttle_patcher.start()
        self.addCleanup(self.throttle_patcher.stop)
    
    def test_login_success(self):
        """Test la connexion réussie"""
        data = {
            'username': 'testuser',
            'password': 'testpass123',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertIn('user', response.data)
    
    def test_login_wrong_password(self):
        """Test la connexion avec un mauvais mot de passe"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_nonexistent_user(self):
        """Test la connexion avec un utilisateur inexistant"""
        data = {
            'username': 'nonexistent',
            'password': 'testpass123',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_missing_credentials(self):
        """Test la connexion sans credentials"""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(WAF_BLOCK_MODE=False, REST_FRAMEWORK={'DEFAULT_THROTTLE_CLASSES': [], 'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication']})
class UserProfileAPITestCase(APITestCase):
    """Tests pour l'endpoint de profil utilisateur"""
    
    def setUp(self):
        """Configuration initiale"""
        self.client = APIClient()
        self.user = UserFactory(username='testuser')
        self.url = '/api/auth/profile/'
        
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
        
        # Disable throttling
        from rest_framework.throttling import UserRateThrottle
        self.throttle_patcher = unittest.mock.patch.object(UserRateThrottle, 'allow_request', return_value=True)
        self.throttle_patcher.start()
        self.addCleanup(self.throttle_patcher.stop)
    
    def test_get_profile_authenticated(self):
        """Test récupérer le profil quand authentifié"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')
    
    def test_get_profile_unauthenticated(self):
        """Test récupérer le profil sans authentification"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_profile(self):
        """Test mettre à jour le profil"""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '+33612345678',
            'company_name': 'New Company',
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier en base de données
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.phone, '+33612345678')
    
    def test_cannot_update_username(self):
        """Test qu'un utilisateur ne peut pas changer son username"""
        original_username = self.user.username
        data = {'username': 'newusername'}
        response = self.client.patch(self.url, data, format='json')
        
        self.user.refresh_from_db()
        # Le username ne devrait pas avoir changé
        self.assertEqual(self.user.username, original_username)


@override_settings(WAF_BLOCK_MODE=False, REST_FRAMEWORK={'DEFAULT_THROTTLE_CLASSES': [], 'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication']})
class TokenRefreshAPITestCase(APITestCase):
    """Tests pour le rafraîchissement de token"""
    
    def setUp(self):
        """Configuration initiale"""
        self.client = APIClient()
        self.user = UserFactory(username='testuser')
        
        # Se connecter pour obtenir les tokens
        login_url = '/api/auth/login/'
        login_data = {
            'username': 'testuser',
            'password': 'testpass123',
        }
        response = self.client.post(login_url, login_data)
        self.refresh_token = response.data['tokens']['refresh']
        self.access_token = response.data['tokens']['access']
    
    def test_refresh_token_success(self):
        """Test le rafraîchissement réussi du token"""
        url = '/api/auth/token/refresh/'
        data = {'refresh': self.refresh_token}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data) # Refresh endpoint usually returns access directly or in tokens?
        # Let's check TokenRefreshView behavior. Standard SimpleJWT returns {'access': ...} or {'access': ..., 'refresh': ...}
        # If I customized it, I need to check.
        # But the error was in setUp, so the login response structure was the issue.
        # The refresh endpoint response structure might be standard.
        # I'll assume standard for now, but if it fails I'll check.
    
    def test_refresh_token_invalid(self):
        """Test le rafraîchissement avec un token invalide"""
        url = '/api/auth/token/refresh/'
        data = {'refresh': 'invalid-token'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# ============================================================
# TESTS DE PERMISSIONS
# ============================================================

@override_settings(WAF_BLOCK_MODE=False)
class UserPermissionsTestCase(APITestCase):
    """Tests pour les permissions utilisateur"""
    
    def setUp(self):
        """Configuration initiale"""
        self.client = APIClient()
        self.regular_user = UserFactory(username='regular')
        self.admin_user = AdminUserFactory(username='admin')
    
    def test_regular_user_cannot_access_admin_panel(self):
        """Test qu'un utilisateur normal ne peut pas accéder à l'admin"""
        self.assertFalse(self.regular_user.is_staff)
        self.assertFalse(self.regular_user.is_admin_user)
    
    def test_admin_user_can_access_admin_panel(self):
        """Test qu'un admin peut accéder à l'admin"""
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_admin_user)


 