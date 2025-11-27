from django.contrib.sitemaps import Sitemap
from django.conf import settings
from .models import Project

class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Retourne l'URL du frontend pour ce projet
        return f"/portfolio/{obj.slug}"

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return ['home', 'portfolio', 'contact', 'login', 'register']

    def location(self, item):
        # Mapping des noms de vues vers les URLs frontend
        mapping = {
            'home': '/',
            'portfolio': '/portfolio',
            'contact': '/contact',
            'login': '/login',
            'register': '/register',
        }
        return mapping.get(item, '/')
