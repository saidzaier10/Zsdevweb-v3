"""
Commande pour ajouter de nouvelles options SEO et types de projets WordPress/Shopify
"""
from django.core.management.base import BaseCommand
from quotes.models import ProjectType, SupplementaryOption
from decimal import Decimal


class Command(BaseCommand):
    help = 'Ajoute des options SEO avancées et types de projets WordPress/Shopify'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Ajout de nouvelles options...'))

        # 1. Ajouter de nouveaux types de projets WordPress et Shopify
        new_project_types = [
            {
                'name': 'Site WordPress Vitrine',
                'description': 'Site vitrine développé avec WordPress. Installation, thème premium, personnalisation, plugins essentiels, formation incluse.',
                'base_price': Decimal('2200.00'),
                'estimated_days': 8,
            },
            {
                'name': 'Site WordPress Blog/Magazine',
                'description': 'Blog ou magazine WordPress professionnel. Thème optimisé, catégories, système de commentaires, newsletter, SEO.',
                'base_price': Decimal('2800.00'),
                'estimated_days': 12,
            },
            {
                'name': 'Site WordPress E-commerce (WooCommerce)',
                'description': 'Boutique en ligne complète avec WooCommerce. Gestion produits, paiement sécurisé, livraison, stocks, emails automatiques.',
                'base_price': Decimal('4500.00'),
                'estimated_days': 20,
            },
            {
                'name': 'Boutique Shopify Standard',
                'description': 'E-commerce Shopify clé en main. Configuration complète, thème personnalisé, produits, paiements, expédition, formation.',
                'base_price': Decimal('3500.00'),
                'estimated_days': 15,
            },
            {
                'name': 'Boutique Shopify Premium',
                'description': 'E-commerce Shopify haut de gamme. Design sur mesure, apps premium, intégrations avancées, automatisations, marketing.',
                'base_price': Decimal('6500.00'),
                'estimated_days': 25,
            },
            {
                'name': 'Migration WordPress',
                'description': 'Migration complète de votre site existant vers WordPress. Sauvegarde, transfert contenu, redirections, tests, optimisation.',
                'base_price': Decimal('1500.00'),
                'estimated_days': 7,
            },
            {
                'name': 'Migration Shopify',
                'description': 'Migration de votre boutique vers Shopify. Import produits, clients, commandes, configuration complète, tests, formation.',
                'base_price': Decimal('2500.00'),
                'estimated_days': 10,
            },
        ]

        self.stdout.write('\n📦 Ajout des types de projets WordPress et Shopify...\n')
        for pt_data in new_project_types:
            pt, created = ProjectType.objects.update_or_create(
                name=pt_data['name'],
                defaults=pt_data
            )
            action = "créé" if created else "mis à jour"
            self.stdout.write(f'  ✓ Type de projet "{pt.name}" {action}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(new_project_types)} types de projets ajoutés\n'))

        # 2. Ajouter de nouvelles options SEO avancées
        new_seo_options = [
            {
                'name': 'SEO Local (Google My Business)',
                'description': 'Optimisation SEO local : création/optimisation Google My Business, citations locales, avis clients, rich snippets.',
                'price': Decimal('350.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Audit SEO Complet',
                'description': 'Audit technique SEO détaillé : analyse complète, rapport avec recommandations, plan d\'action prioritaire.',
                'price': Decimal('600.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Stratégie de Contenu SEO',
                'description': 'Stratégie éditoriale SEO : recherche mots-clés, planning éditorial 6 mois, brief rédactionnels, optimisation sémantique.',
                'price': Decimal('450.00'),
                'billing_type': 'monthly',
            },
            {
                'name': 'Link Building (Netlinking)',
                'description': 'Campagne de netlinking mensuelle : acquisition 10 backlinks qualité, articles sponsorisés, suivi positions.',
                'price': Decimal('500.00'),
                'billing_type': 'monthly',
            },
            {
                'name': 'Optimisation Core Web Vitals',
                'description': 'Optimisation performance et Core Web Vitals : compression images, lazy loading, cache, CDN, score 90+ garantie.',
                'price': Decimal('700.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Rédaction SEO (5 articles/mois)',
                'description': 'Rédaction SEO professionnelle : 5 articles optimisés/mois (800-1200 mots), mots-clés ciblés, méta-descriptions.',
                'price': Decimal('400.00'),
                'billing_type': 'monthly',
            },
            {
                'name': 'Schema Markup Avancé',
                'description': 'Implémentation schema.org avancé : rich snippets, FAQ, produits, événements, organisation, améliore CTR.',
                'price': Decimal('400.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'SEO E-commerce',
                'description': 'Optimisation SEO spécifique e-commerce : fiches produits, catégories, filtres, pagination, données structurées.',
                'price': Decimal('800.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Suivi SEO Mensuel',
                'description': 'Suivi et reporting SEO mensuel : positions, trafic organique, conversions, recommandations, ajustements.',
                'price': Decimal('250.00'),
                'billing_type': 'monthly',
            },
        ]

        self.stdout.write('\n🔍 Ajout des options SEO avancées...\n')
        for so_data in new_seo_options:
            so, created = SupplementaryOption.objects.update_or_create(
                name=so_data['name'],
                defaults=so_data
            )
            action = "créée" if created else "mise à jour"
            self.stdout.write(f'  ✓ Option "{so.name}" {action}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(new_seo_options)} options SEO ajoutées\n'))

        # 3. Ajouter d'autres options utiles pour WordPress et Shopify
        new_platform_options = [
            {
                'name': 'Plugins Premium WordPress (Pack)',
                'description': 'Pack de plugins premium WordPress : SEO (Yoast/Rank Math), sécurité (Wordfence), cache (WP Rocket), backups.',
                'price': Decimal('300.00'),
                'billing_type': 'yearly',
            },
            {
                'name': 'Thème WordPress Premium',
                'description': 'Thème WordPress premium professionnel avec licence : design moderne, responsive, nombreuses démos.',
                'price': Decimal('150.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Formation WordPress Avancée',
                'description': 'Formation WordPress complète : gestion contenu, SEO, sécurité, extensions, maintenance. 4h en visio + documentation.',
                'price': Decimal('500.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Shopify Apps Premium (Pack)',
                'description': 'Pack d\'applications Shopify premium : avis clients, upsell, emails, chat, récupération panier abandonné.',
                'price': Decimal('80.00'),
                'billing_type': 'monthly',
            },
            {
                'name': 'Thème Shopify Premium',
                'description': 'Thème Shopify premium personnalisé avec licence : design professionnel, conversion optimisée, mobile-first.',
                'price': Decimal('250.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Intégration Shopify Multi-canal',
                'description': 'Intégration ventes multi-canal : Facebook Shop, Instagram Shopping, Google Shopping, Amazon, marketplaces.',
                'price': Decimal('600.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Formation Shopify Complète',
                'description': 'Formation Shopify approfondie : produits, collections, marketing, apps, analytics, optimisation. 5h + support 30j.',
                'price': Decimal('600.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Configuration Email Marketing (Klaviyo/Mailchimp)',
                'description': 'Configuration email marketing e-commerce : automatisations (panier abandonné, welcome, post-achat), templates.',
                'price': Decimal('500.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Optimisation Conversion E-commerce',
                'description': 'Audit et optimisation conversion : A/B testing, parcours client, checkout, urgence, preuve sociale, garanties.',
                'price': Decimal('900.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Import/Migration Produits',
                'description': 'Import massif de produits : préparation fichiers, import, images, catégories, variants, stocks. Jusqu\'à 500 produits.',
                'price': Decimal('800.00'),
                'billing_type': 'one_time',
            },
        ]

        self.stdout.write('\n💼 Ajout des options WordPress et Shopify...\n')
        for po_data in new_platform_options:
            po, created = SupplementaryOption.objects.update_or_create(
                name=po_data['name'],
                defaults=po_data
            )
            action = "créée" if created else "mise à jour"
            self.stdout.write(f'  ✓ Option "{po.name}" {action}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(new_platform_options)} options plateforme ajoutées\n'))

        # Résumé final
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('🎉 AJOUT DES NOUVELLES OPTIONS TERMINÉ !'))
        self.stdout.write(self.style.SUCCESS('='*60))

        total_project_types = ProjectType.objects.count()
        total_options = SupplementaryOption.objects.count()

        self.stdout.write(f'\n📊 Résumé :')
        self.stdout.write(f'   • {total_project_types} types de projets au total')
        self.stdout.write(f'   • {total_options} options supplémentaires au total')
        self.stdout.write(f'\n   Nouveaux ajouts :')
        self.stdout.write(f'   • {len(new_project_types)} types de projets (WordPress/Shopify)')
        self.stdout.write(f'   • {len(new_seo_options)} options SEO avancées')
        self.stdout.write(f'   • {len(new_platform_options)} options WordPress/Shopify')

        self.stdout.write(f'\n📝 Prochaines étapes :')
        self.stdout.write(f'   1. Testez la création de devis avec les nouvelles options')
        self.stdout.write(f'   2. Accédez à l\'admin : http://localhost:8000/admin')
        self.stdout.write(f'   3. Personnalisez les prix selon vos besoins')
        self.stdout.write('')
