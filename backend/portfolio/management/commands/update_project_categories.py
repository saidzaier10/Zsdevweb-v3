"""
Commande pour mettre à jour les catégories des projets existants
"""
from django.core.management.base import BaseCommand
from portfolio.models import Project


class Command(BaseCommand):
    help = 'Met à jour les catégories des projets existants en fonction de leur titre'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Mise à jour des catégories des projets...'))

        # Règles de catégorisation basées sur les titres/descriptions
        categorization_rules = {
            'ecommerce': [
                'e-commerce', 'ecommerce', 'boutique', 'shop', 'woocommerce', 'shopify',
                'panier', 'paiement', 'vente en ligne', 'magasin'
            ],
            'mobile': [
                'mobile', 'app', 'application', 'ios', 'android', 'react native',
                'flutter', 'swift', 'kotlin'
            ],
            'api': [
                'api', 'rest', 'graphql', 'backend', 'microservice'
            ],
        }

        projects = Project.objects.all()
        updated_count = 0

        for project in projects:
            # Texte à analyser (titre + description en minuscules)
            text = f"{project.title} {project.short_description}".lower()

            # Déterminer la catégorie
            category = 'web'  # Par défaut

            # Vérifier chaque catégorie
            for cat, keywords in categorization_rules.items():
                if any(keyword in text for keyword in keywords):
                    category = cat
                    break

            # Mettre à jour si nécessaire
            if project.category != category:
                old_category = project.category
                project.category = category
                project.save(update_fields=['category'])
                updated_count += 1
                self.stdout.write(
                    f'  ✓ "{project.title}": {old_category} → {category}'
                )
            else:
                self.stdout.write(
                    f'  - "{project.title}": {category} (inchangé)'
                )

        self.stdout.write(self.style.SUCCESS(f'\n✅ {updated_count} projet(s) mis à jour'))
        self.stdout.write(self.style.SUCCESS(f'   {projects.count() - updated_count} projet(s) déjà à jour'))

        # Afficher la répartition par catégorie
        self.stdout.write('\n📊 Répartition par catégorie:')
        for category, label in Project.CATEGORY_CHOICES:
            count = Project.objects.filter(category=category).count()
            if count > 0:
                self.stdout.write(f'   • {label}: {count} projet(s)')
