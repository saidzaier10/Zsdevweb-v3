"""
Script de configuration des catégories et associations intelligentes
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from quotes.models import ProjectCategory, ProjectType, SupplementaryOption


class Command(BaseCommand):
    help = 'Configure les catégories de projets et les associations intelligentes'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.stdout.write('\n🚀 Configuration des catégories...\n')

            # Créer les 3 catégories principales
            categories_data = [
                {
                    'name': 'Site Vitrine',
                    'slug': 'site-vitrine',
                    'description': 'Sites web de présentation pour entreprises, associations ou particuliers',
                    'icon': 'fas fa-globe',
                    'color': '#3b82f6',
                    'order': 1
                },
                {
                    'name': 'E-commerce',
                    'slug': 'e-commerce',
                    'description': 'Boutiques en ligne et plateformes de vente',
                    'icon': 'fas fa-shopping-cart',
                    'color': '#10b981',
                    'order': 2
                },
                {
                    'name': 'Application Web',
                    'slug': 'application-web',
                    'description': 'Applications web sur mesure, plateformes SaaS et solutions métier',
                    'icon': 'fas fa-code',
                    'color': '#8b5cf6',
                    'order': 3
                }
            ]

            categories = {}
            for cat_data in categories_data:
                cat, created = ProjectCategory.objects.get_or_create(
                    slug=cat_data['slug'],
                    defaults=cat_data
                )
                categories[cat.slug] = cat
                status = '✨ Créée' if created else '✓ Existe'
                self.stdout.write(f'  {status}: {cat.name}')

            self.stdout.write('\n📦 Association des types de projets...\n')

            # Mapping des types de projets vers les catégories
            project_mappings = {
                'Site Vitrine': 'site-vitrine',
                'Site WordPress Vitrine': 'site-vitrine',
                'Landing Page': 'site-vitrine',
                'Portfolio': 'site-vitrine',
                'Blog / Magazine': 'site-vitrine',
                'Site WordPress Blog/Magazine': 'site-vitrine',

                'E-commerce': 'e-commerce',
                'Site WordPress E-commerce (WooCommerce)': 'e-commerce',
                'Boutique Shopify Standard': 'e-commerce',
                'Boutique Shopify Premium': 'e-commerce',
                'Migration Shopify': 'e-commerce',
                'Migration WordPress': 'e-commerce',
                'Marketplace': 'e-commerce',

                'Application Web': 'application-web',
                'Plateforme SaaS': 'application-web',
            }

            for project_name, category_slug in project_mappings.items():
                try:
                    project = ProjectType.objects.get(name=project_name)
                    project.category = categories[category_slug]
                    project.save(update_fields=['category'])
                    self.stdout.write(f'  ✓ {project_name} → {categories[category_slug].name}')
                except ProjectType.DoesNotExist:
                    self.stdout.write(f'  ⚠️  Type "{project_name}" non trouvé')

            self.stdout.write('\n🔧 Configuration des options compatibles...\n')

            # Options spécifiques à SITE VITRINE
            vitrine_options = [
                'Charte graphique complète',
                'Création de logo',
                'Formation',
                'Blog / Magazine',
                'Portfolio',
                'Intégration Newsletter',
                'Formation WordPress Avancée',
                'Optimisation SEO',
                'Rédaction de contenu',
                'Photographie professionnelle',
                'Vidéo de présentation',
            ]

            # Options spécifiques à E-COMMERCE
            ecommerce_options = [
                'Passerelle de paiement avancée',
                'Gestion des stocks',
                'Programme de fidélité',
                'Intégration Marketplace',
                'Boutique Shopify Standard',
                'Boutique Shopify Premium',
                'Formation Shopify Complète',
                'Configuration Email Marketing (Klaviyo/Mailchimp)',
                'Intégration Shopify Multi-canal',
                'Import/Migration Produits',
                'Site WordPress E-commerce (WooCommerce)',
            ]

            # Options spécifiques à APPLICATION WEB
            application_options = [
                'Application Mobile',
                'Intégration CRM',
                'Espace Membre',
                'API REST',
                'Tableau de bord analytics',
                'Système de notifications',
                'Authentification avancée',
                'Plateforme SaaS',
                'Système de tickets',
                'Chat en temps réel',
            ]

            # Options communes à toutes les catégories
            common_options = [
                'Hébergement Standard',
                'Hébergement Premium',
                'Maintenance Basique',
                'Maintenance Premium',
                'Certificat SSL Premium',
                'Analytics et Reporting',
                'Audit SEO Complet',
                'Link Building (Netlinking)',
                'Référencement Google Ads',
                'Référencement Social Media',
            ]

            # Configurer les options SITE VITRINE
            for option_name in vitrine_options:
                try:
                    option = SupplementaryOption.objects.get(name__icontains=option_name.split('(')[0].strip())
                    option.compatible_categories.add(categories['site-vitrine'])
                    self.stdout.write(f'  ✓ {option.name} → Site Vitrine')
                except SupplementaryOption.DoesNotExist:
                    pass
                except SupplementaryOption.MultipleObjectsReturned:
                    options = SupplementaryOption.objects.filter(name__icontains=option_name.split('(')[0].strip())
                    for opt in options:
                        opt.compatible_categories.add(categories['site-vitrine'])
                        self.stdout.write(f'  ✓ {opt.name} → Site Vitrine')

            # Configurer les options E-COMMERCE
            for option_name in ecommerce_options:
                try:
                    option = SupplementaryOption.objects.get(name__icontains=option_name.split('(')[0].strip())
                    option.compatible_categories.add(categories['e-commerce'])
                    self.stdout.write(f'  ✓ {option.name} → E-commerce')
                except SupplementaryOption.DoesNotExist:
                    pass
                except SupplementaryOption.MultipleObjectsReturned:
                    options = SupplementaryOption.objects.filter(name__icontains=option_name.split('(')[0].strip())
                    for opt in options:
                        opt.compatible_categories.add(categories['e-commerce'])
                        self.stdout.write(f'  ✓ {opt.name} → E-commerce')

            # Configurer les options APPLICATION WEB
            for option_name in application_options:
                try:
                    option = SupplementaryOption.objects.get(name__icontains=option_name.split('(')[0].strip())
                    option.compatible_categories.add(categories['application-web'])
                    self.stdout.write(f'  ✓ {option.name} → Application Web')
                except SupplementaryOption.DoesNotExist:
                    pass
                except SupplementaryOption.MultipleObjectsReturned:
                    options = SupplementaryOption.objects.filter(name__icontains=option_name.split('(')[0].strip())
                    for opt in options:
                        opt.compatible_categories.add(categories['application-web'])
                        self.stdout.write(f'  ✓ {opt.name} → Application Web')

            # Les options communes n'ont pas besoin d'être assignées (elles restent universelles)
            self.stdout.write(f'\n✅ Options communes ({len(common_options)}) : disponibles pour toutes les catégories\n')

            # Statistiques finales
            self.stdout.write('\n📊 Statistiques finales:\n')
            for category in ProjectCategory.objects.all():
                project_count = category.project_types.count()
                option_count = category.compatible_options.count()
                universal_options = SupplementaryOption.objects.filter(compatible_categories__isnull=True).count()
                self.stdout.write(
                    f'  • {category.name}: {project_count} types de projets, '
                    f'{option_count} options spécifiques + {universal_options} options universelles'
                )

            self.stdout.write(self.style.SUCCESS('\n✨ Configuration terminée avec succès!\n'))
