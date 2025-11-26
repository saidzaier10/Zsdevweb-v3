"""
Tests unitaires pour l'app quotes
"""
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from .models import Quote, ProjectType, ProjectCategory, DesignOption, ComplexityLevel, QuoteTemplate
from users.factories import UserFactory

class QuoteModelTestCase(TestCase):
    """Tests pour le modèle Quote"""

    def setUp(self):
        self.user = UserFactory()
        
        # Créer les dépendances nécessaires
        self.category = ProjectCategory.objects.create(name="Web", slug="web")
        self.project_type = ProjectType.objects.create(
            name="Site Vitrine", 
            category=self.category,
            base_price=Decimal('1000.00')
        )
        self.design = DesignOption.objects.create(
            name="Modern", 
            description="Modern design",
            price_supplement=Decimal('500.00')
        )
        self.complexity = ComplexityLevel.objects.create(
            name="Basic", 
            description="Basic complexity",
            price_multiplier=Decimal('1.0')
        )
        
        self.quote = Quote.objects.create(
            client_name="Client Test",
            client_email="client@test.com",
            project_type=self.project_type,
            design_option=self.design,
            complexity_level=self.complexity,
            project_description="Test description"
        )

    def test_quote_calculation(self):
        """Test le calcul du total du devis"""
        # Base 1000 + Design 500 = 1500 * Complexity 1.0 = 1500
        # TVA 20% = 300
        # Total TTC = 1800
        self.quote.save() # Trigger calculation
        self.assertEqual(self.quote.subtotal_ht, Decimal('1500.00'))
        self.assertEqual(self.quote.total_ttc, Decimal('1800.00'))

    def test_quote_str(self):
        """Test la représentation string"""
        self.assertTrue(str(self.quote).startswith("Devis #"))


@override_settings(WAF_BLOCK_MODE=False)
class QuoteAPITestCase(APITestCase):
    """Tests pour l'API quotes"""

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = '/api/quotes/quotes/'
        
        # Créer les dépendances
        self.category = ProjectCategory.objects.create(name="Web", slug="web")
        self.project_type = ProjectType.objects.create(
            name="Site Vitrine", 
            category=self.category,
            base_price=Decimal('1000.00')
        )
        self.design = DesignOption.objects.create(
            name="Modern", 
            description="Modern design",
            price_supplement=Decimal('500.00')
        )
        self.complexity = ComplexityLevel.objects.create(
            name="Basic", 
            description="Basic complexity",
            price_multiplier=Decimal('1.0')
        )
        
        self.quote = Quote.objects.create(
            client_name="Test Client",
            client_email="client@test.com",
            project_type=self.project_type,
            design_option=self.design,
            complexity_level=self.complexity,
            project_description="Test Quote",
            created_by=self.user,
            status='sent'
        )

    def test_create_quote(self):
        """Test la création d'un devis"""
        data = {
            'client_name': 'New Client',
            'client_email': 'new@client.com',
            'project_type': self.project_type.id,
            'design_option': self.design.id,
            'complexity_level': self.complexity.id,
            'project_description': 'New project desc'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quote.objects.count(), 2)
        quote = Quote.objects.get(client_name='New Client')
        self.assertEqual(quote.client_name, 'New Client')
        self.assertEqual(quote.subtotal_ht, Decimal('1500.00'))

    def test_duplicate_quote(self):
        """Test la duplication d'un devis"""
        self.client.force_authenticate(user=self.user)
        url = f'{self.url}{self.quote.id}/duplicate/'
        response = self.client.post(url)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Duplicate Error: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quote.objects.count(), 2)
        new_quote = Quote.objects.exclude(id=self.quote.id).first()
        self.assertEqual(new_quote.client_name, self.quote.client_name)
        self.assertNotEqual(new_quote.quote_number, self.quote.quote_number)

    def test_sign_quote(self):
        """Test la signature d'un devis"""
        url = f'{self.url}sign/{self.quote.signature_token}/'
        data = {
            'signature': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
            'signer_name': 'Client Name',
            'terms_accepted': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quote.refresh_from_db()
        self.assertEqual(self.quote.status, 'accepted')
        self.assertIsNotNone(self.quote.signed_at)

    def test_reject_quote(self):
        """Test le rejet d'un devis"""
        self.client.force_authenticate(user=self.user) # Assuming user can reject their own quote or public action?
        # The view uses get_object() which filters by permission. 
        # If public rejection is needed, it should be a public action. 
        # The current view implementation for reject is detail=True, so it uses standard permissions (IsAuthenticated for owner).
        url = f'{self.url}{self.quote.id}/reject/'
        data = {'reason': 'Too expensive'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quote.refresh_from_db()
        self.assertEqual(self.quote.status, 'rejected')
        self.assertEqual(self.quote.rejection_reason, 'Too expensive')


@override_settings(WAF_BLOCK_MODE=False)
class ReferenceDataAPITestCase(APITestCase):
    """Tests pour les données de référence (Categories, Types, etc.)"""

    def setUp(self):
        self.client = APIClient()
        self.category = ProjectCategory.objects.create(name="Web", slug="web")
        self.project_type = ProjectType.objects.create(name="Site Vitrine", category=self.category, base_price=Decimal('1000'))

    def test_list_categories(self):
        url = '/api/quotes/categories/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_project_types(self):
        url = '/api/quotes/project-types/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


@override_settings(WAF_BLOCK_MODE=False)
class QuoteTemplateAPITestCase(APITestCase):
    """Tests pour les templates de devis"""

    def setUp(self):
        self.client = APIClient()
        self.admin = UserFactory(username='admin', is_staff=True)
        self.category = ProjectCategory.objects.create(name="Web", slug="web")
        self.project_type = ProjectType.objects.create(name="Site Vitrine", category=self.category, base_price=Decimal('1000'))
        self.design = DesignOption.objects.create(name="Modern", price_supplement=Decimal('500'))
        self.complexity = ComplexityLevel.objects.create(name="Basic", price_multiplier=Decimal('1.0'))
        

        
        self.template = QuoteTemplate.objects.create(
            name="Standard Web",
            project_type=self.project_type,
            design_option=self.design,
            complexity_level=self.complexity,
            default_description="Default desc"
        )

    def test_list_templates(self):
        url = '/api/quotes/templates/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_template_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = '/api/quotes/templates/'
        data = {
            'name': 'New Template',
            'project_type': self.project_type.id,
            'design_option': self.design.id,
            'complexity_level': self.complexity.id,
            'default_description': 'New desc'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

