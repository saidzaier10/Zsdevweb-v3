"""
Tests unitaires pour l'app portfolio
"""
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Technology, Project, Testimonial, ContactMessage
from users.factories import AdminUserFactory

class PortfolioModelTestCase(TestCase):
    """Tests pour les modèles du portfolio"""

    def setUp(self):
        self.tech = Technology.objects.create(name="Python", icon="python-icon", category="backend")
        # Valid 1x1 GIF
        image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        image = SimpleUploadedFile("test.gif", image_content, content_type="image/gif")
        self.project = Project.objects.create(
            title="Test Project",
            slug="test-project",
            description="A test project description",
            category="web",
            image_main=image
        )
        self.project.technologies.add(self.tech)

    def test_project_creation(self):
        """Test la création d'un projet"""
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.category, "web")
        self.assertIn(self.tech, self.project.technologies.all())

    def test_project_str(self):
        """Test la représentation string"""
        self.assertEqual(str(self.project), "Test Project")


@override_settings(WAF_BLOCK_MODE=False)
class PortfolioAPITestCase(APITestCase):
    """Tests pour l'API portfolio"""

    def setUp(self):
        self.client = APIClient()
        # Set a valid User-Agent to bypass SecurityMiddleware
        self.client.defaults['HTTP_USER_AGENT'] = 'Mozilla/5.0 (Test Client)'
        
        self.admin = AdminUserFactory()
        # Valid 1x1 GIF
        image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        image = SimpleUploadedFile("test.gif", image_content, content_type="image/gif")
        self.project = Project.objects.create(
            title="Test Project",
            slug="test-project",
            description="A test project description",
            category="web",
            image_main=image,
            is_published=True
        )

    def test_list_projects(self):
        """Test la liste des projets (public)"""
        url = '/api/portfolio/projects/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Test Project")

    def test_create_project_unauthorized(self):
        """Test qu'un anonyme ne peut pas créer de projet"""
        url = '/api/portfolio/projects/'
        data = {'title': 'New Project'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project_admin(self):
        """Test qu'un admin peut créer un projet"""
        self.client.force_authenticate(user=self.admin)
        url = '/api/portfolio/projects/'
        
        # Image fictive pour le test (Valid GIF)
        image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        image = SimpleUploadedFile("test_image.gif", image_content, content_type="image/gif")
        
        data = {
            'title': 'Admin Project',
            'slug': 'admin-project',
            'short_description': 'Short desc',
            'description': 'Created by admin',
            'category': 'web',
            'image_main': image,
            'is_published': True
        }
        response = self.client.post(url, data, format='multipart')
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(slug='admin-project').exists())

    def test_update_project_admin(self):
        """Test qu'un admin peut modifier un projet"""
        self.client.force_authenticate(user=self.admin)
        url = f'/api/portfolio/projects/{self.project.id}/'
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Title')

    def test_delete_project_admin(self):
        """Test qu'un admin peut supprimer un projet"""
        self.client.force_authenticate(user=self.admin)
        url = f'/api/portfolio/projects/{self.project.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())


@override_settings(WAF_BLOCK_MODE=False)
class TechnologyAPITestCase(APITestCase):
    """Tests pour l'API technologies"""

    def setUp(self):
        self.client = APIClient()
        self.tech = Technology.objects.create(name="Python", icon="python-icon", category="backend")

    def test_list_technologies(self):
        """Test la liste des technologies"""
        url = '/api/portfolio/technologies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertGreaterEqual(len(results), 1)
        # Check if our created tech is in the list
        names = [t['name'] for t in results]
        self.assertIn('Python', names)


@override_settings(WAF_BLOCK_MODE=False)
class TestimonialAPITestCase(APITestCase):
    """Tests pour l'API témoignages"""

    def setUp(self):
        self.client = APIClient()
        self.testimonial = Testimonial.objects.create(
            client_name="Happy Client",
            content="Great work!",
            rating=5,
            is_published=True
        )

    def test_list_testimonials(self):
        """Test la liste des témoignages"""
        url = '/api/portfolio/testimonials/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertGreaterEqual(len(results), 1)
        # Check if our created testimonial is in the list
        clients = [t['client_name'] for t in results]
        self.assertIn('Happy Client', clients)


@override_settings(WAF_BLOCK_MODE=False)
class ContactMessageAPITestCase(APITestCase):
    """Tests pour l'API contact"""

    def setUp(self):
        self.client = APIClient()
        self.admin = AdminUserFactory()
        self.url = '/api/portfolio/contact/'

    def test_create_contact_message(self):
        """Test la création d'un message de contact (public)"""
        data = {
            'name': 'Contact Person',
            'email': 'contact@example.com',
            'subject': 'Inquiry',
            'message': 'Hello there!'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ContactMessage.objects.filter(email='contact@example.com').exists())

    def test_list_messages_admin(self):
        """Test la liste des messages (admin only)"""
        ContactMessage.objects.create(name='Sender', email='sender@test.com', message='Msg')
        
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertGreaterEqual(len(results), 1)

    def test_list_messages_anonymous_forbidden(self):
        """Test qu'un anonyme ne peut pas lister les messages"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
