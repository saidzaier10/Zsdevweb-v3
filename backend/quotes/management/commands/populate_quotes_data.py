"""
Commande pour peupler la base de données avec des données de test
"""
from django.core.management.base import BaseCommand
from quotes.models import (
    Company,
    ProjectType,
    DesignOption,
    ComplexityLevel,
    SupplementaryOption,
    QuoteTemplate
)


class Command(BaseCommand):
    help = 'Peuple la base de données avec des données de test pour les devis'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Début du peuplement de la base de données...'))
        
        # 1. Créer/Mettre à jour l'entreprise
        company, created = Company.objects.get_or_create(id=1)
        company.name = "ZSdevweb"
        company.email = "contact@zsdevweb.com"
        company.phone = "+33 6 12 34 56 78"
        company.address = "123 Rue du Code\n75001 Paris, France"
        company.siret = "12345678900014"
        company.tva_number = "FR12345678900"
        company.primary_color = "#1a56db"
        company.footer_text = "Merci de votre confiance | www.zsdevweb.com | contact@zsdevweb.com"
        company.email_signature = "Cordialement,\nL'équipe ZSdevweb\n\n📧 contact@zsdevweb.com\n📱 +33 6 12 34 56 78"
        company.save()
        self.stdout.write(self.style.SUCCESS('✓ Entreprise configurée'))
        
        # 2. Types de projets
        project_types = [
            {
                'name': 'Site Vitrine',
                'description': 'Site web de présentation pour entreprise ou professionnel',
                'base_price': 1500.00,
                'estimated_days': 10
            },
            {
                'name': 'Site E-commerce',
                'description': 'Boutique en ligne avec paiement sécurisé',
                'base_price': 3500.00,
                'estimated_days': 20
            },
            {
                'name': 'Application Web',
                'description': 'Application web sur mesure avec fonctionnalités complexes',
                'base_price': 5000.00,
                'estimated_days': 30
            },
            {
                'name': 'Blog / Site de Contenu',
                'description': 'Site orienté contenu avec système de gestion d\'articles',
                'base_price': 1200.00,
                'estimated_days': 8
            },
            {
                'name': 'Portfolio',
                'description': 'Site portfolio pour artiste, photographe ou créatif',
                'base_price': 1000.00,
                'estimated_days': 7
            },
        ]
        
        for pt_data in project_types:
            ProjectType.objects.get_or_create(
                name=pt_data['name'],
                defaults=pt_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(project_types)} types de projets créés'))
        
        # 3. Options de design
        design_options = [
            {
                'name': 'Design Simple',
                'description': 'Design épuré et fonctionnel',
                'price_supplement': 0.00
            },
            {
                'name': 'Design Moderne',
                'description': 'Design contemporain avec animations',
                'price_supplement': 500.00
            },
            {
                'name': 'Design Premium',
                'description': 'Design sur mesure avec interactions avancées',
                'price_supplement': 1200.00
            },
        ]
        
        for do_data in design_options:
            DesignOption.objects.get_or_create(
                name=do_data['name'],
                defaults=do_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(design_options)} options de design créées'))
        
        # 4. Niveaux de complexité
        complexity_levels = [
            {
                'name': 'Basique',
                'description': 'Fonctionnalités standards',
                'price_multiplier': 1.0
            },
            {
                'name': 'Intermédiaire',
                'description': 'Fonctionnalités avancées',
                'price_multiplier': 1.3
            },
            {
                'name': 'Avancé',
                'description': 'Fonctionnalités complexes et intégrations',
                'price_multiplier': 1.7
            },
        ]
        
        for cl_data in complexity_levels:
            ComplexityLevel.objects.get_or_create(
                name=cl_data['name'],
                defaults=cl_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(complexity_levels)} niveaux de complexité créés'))
        
        # 5. Options supplémentaires
        supplementary_options = [
            {
                'name': 'Référencement SEO',
                'description': 'Optimisation pour les moteurs de recherche',
                'price': 300.00,
                'billing_type': 'one_time'
            },
            {
                'name': 'Hébergement Premium',
                'description': 'Hébergement haute performance avec SSL',
                'price': 25.00,
                'billing_type': 'monthly'
            },
            {
                'name': 'Maintenance',
                'description': 'Maintenance et mises à jour régulières',
                'price': 80.00,
                'billing_type': 'monthly'
            },
            {
                'name': 'Formation',
                'description': 'Formation à l\'utilisation du site (2h)',
                'price': 200.00,
                'billing_type': 'one_time'
            },
            {
                'name': 'Rédaction de contenu',
                'description': 'Rédaction professionnelle de 5 pages',
                'price': 400.00,
                'billing_type': 'one_time'
            },
            {
                'name': 'Multilingue',
                'description': 'Site en plusieurs langues',
                'price': 600.00,
                'billing_type': 'one_time'
            },
            {
                'name': 'Backup quotidien',
                'description': 'Sauvegarde automatique quotidienne',
                'price': 15.00,
                'billing_type': 'monthly'
            },
            {
                'name': 'Certificat SSL Premium',
                'description': 'Certificat SSL avec garantie étendue',
                'price': 150.00,
                'billing_type': 'yearly'
            },
            {
                'name': 'Google Analytics',
                'description': 'Configuration et intégration Google Analytics',
                'price': 150.00,
                'billing_type': 'one_time'
            },
            {
                'name': 'Newsletter',
                'description': 'Système de newsletter avec Mailchimp',
                'price': 250.00,
                'billing_type': 'one_time'
            },
        ]
        
        for so_data in supplementary_options:
            SupplementaryOption.objects.get_or_create(
                name=so_data['name'],
                defaults=so_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(supplementary_options)} options supplémentaires créées'))
        
        # 6. Templates de devis
        templates_data = [
            {
                'name': 'Site Vitrine Standard',
                'description': 'Template pour un site vitrine classique',
                'project_type': 'Site Vitrine',
                'design_option': 'Design Moderne',
                'complexity_level': 'Basique',
                'supplementary_options': ['Référencement SEO', 'Hébergement Premium'],
                'default_description': 'Site vitrine professionnel avec :\n- Page d\'accueil\n- Page À propos\n- Page Services\n- Page Contact\n- Formulaire de contact\n- Design responsive\n- Optimisation SEO de base'
            },
            {
                'name': 'E-commerce Complet',
                'description': 'Template pour une boutique en ligne complète',
                'project_type': 'Site E-commerce',
                'design_option': 'Design Premium',
                'complexity_level': 'Avancé',
                'supplementary_options': ['Référencement SEO', 'Hébergement Premium', 'Maintenance', 'Formation'],
                'default_description': 'Boutique en ligne complète avec :\n- Catalogue produits\n- Panier d\'achat\n- Paiement sécurisé (Stripe, PayPal)\n- Gestion des commandes\n- Espace client\n- Dashboard admin\n- Emails automatiques'
            },
        ]
        
        for template_data in templates_data:
            # Récupérer les objets liés
            project_type = ProjectType.objects.get(name=template_data['project_type'])
            design_option = DesignOption.objects.get(name=template_data['design_option'])
            complexity_level = ComplexityLevel.objects.get(name=template_data['complexity_level'])
            
            template, created = QuoteTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    'description': template_data['description'],
                    'project_type': project_type,
                    'design_option': design_option,
                    'complexity_level': complexity_level,
                    'default_description': template_data['default_description'],
                }
            )
            
            # Ajouter les options supplémentaires
            if created:
                for option_name in template_data['supplementary_options']:
                    option = SupplementaryOption.objects.get(name=option_name)
                    template.supplementary_options.add(option)
        
        self.stdout.write(self.style.SUCCESS(f'✓ {len(templates_data)} templates créés'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Base de données peuplée avec succès !'))
        self.stdout.write(self.style.WARNING('\n📝 Prochaines étapes :'))
        self.stdout.write('   1. Accédez à l\'admin : http://localhost:8000/admin')
        self.stdout.write('   2. Configurez votre logo dans "Entreprise"')
        self.stdout.write('   3. Créez votre premier devis !')