"""
Commande pour peupler la base de données Quotes avec des données de test
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
from decimal import Decimal


class Command(BaseCommand):
    help = 'Peuple la base de données avec des données de test pour les Devis'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Début du peuplement de la base de données Quotes...'))

        # 1. Créer ou mettre à jour les informations de l'entreprise
        company = Company.get_instance()
        company.name = "Zsdevweb"
        company.email = "contact@zsdevweb.com"
        company.phone = "+33 6 12 34 56 78"
        company.address = "123 Rue de la Tech\n75001 Paris, France"
        company.siret = "12345678901234"
        company.tva_number = "FR12345678901"
        company.primary_color = "#1a56db"
        company.footer_text = "Merci de votre confiance | www.zsdevweb.com"
        company.email_signature = "Cordialement,\nL'équipe Zsdevweb"
        company.save()
        self.stdout.write(f'  ✓ Entreprise "{company.name}" configurée')

        self.stdout.write(self.style.SUCCESS('\n✅ Entreprise configurée\n'))

        # 2. Créer les Types de Projets
        project_types_data = [
            {
                'name': 'Site Vitrine',
                'description': 'Site web vitrine pour présenter votre entreprise, vos services et votre expertise. Idéal pour les PME, artisans et professions libérales.',
                'base_price': Decimal('2500.00'),
                'estimated_days': 10,
            },
            {
                'name': 'E-commerce',
                'description': 'Boutique en ligne complète avec gestion des produits, panier, paiement sécurisé et espace client. Pour vendre vos produits en ligne.',
                'base_price': Decimal('5000.00'),
                'estimated_days': 25,
            },
            {
                'name': 'Application Web',
                'description': 'Application web sur mesure pour répondre à vos besoins spécifiques. Gestion, CRM, ERP, plateforme métier.',
                'base_price': Decimal('8000.00'),
                'estimated_days': 40,
            },
            {
                'name': 'Landing Page',
                'description': 'Page de destination optimisée pour la conversion. Parfait pour vos campagnes marketing et lancement de produits.',
                'base_price': Decimal('1200.00'),
                'estimated_days': 5,
            },
            {
                'name': 'Blog / Magazine',
                'description': 'Site de publication de contenus avec système de gestion d\'articles, catégories, commentaires et newsletter.',
                'base_price': Decimal('3000.00'),
                'estimated_days': 15,
            },
            {
                'name': 'Portfolio',
                'description': 'Site portfolio pour présenter vos réalisations, projets et compétences. Idéal pour créatifs, photographes, designers.',
                'base_price': Decimal('1800.00'),
                'estimated_days': 8,
            },
            {
                'name': 'Marketplace',
                'description': 'Plateforme multi-vendeurs permettant à plusieurs marchands de vendre leurs produits. Système de commissions inclus.',
                'base_price': Decimal('12000.00'),
                'estimated_days': 60,
            },
            {
                'name': 'Plateforme SaaS',
                'description': 'Logiciel en ligne accessible par abonnement. Solution complète avec gestion multi-utilisateurs et facturation récurrente.',
                'base_price': Decimal('15000.00'),
                'estimated_days': 80,
            },
        ]

        project_types = {}
        for pt_data in project_types_data:
            pt, created = ProjectType.objects.update_or_create(
                name=pt_data['name'],
                defaults=pt_data
            )
            project_types[pt_data['name']] = pt
            action = "créé" if created else "mis à jour"
            self.stdout.write(f'  ✓ Type de projet "{pt.name}" {action}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(project_types_data)} types de projets synchronisés\n'))

        # 3. Créer les Options de Design
        design_options_data = [
            {
                'name': 'Design Simple',
                'description': 'Design épuré et fonctionnel. Mise en page classique, couleurs sobres, navigation simple. Idéal pour budget serré.',
                'price_supplement': Decimal('0.00'),
            },
            {
                'name': 'Design Moderne',
                'description': 'Design contemporain et attractif. Animations subtiles, mise en page moderne, palette de couleurs harmonieuse.',
                'price_supplement': Decimal('800.00'),
            },
            {
                'name': 'Design Premium',
                'description': 'Design haut de gamme et personnalisé. Animations avancées, interactions riches, identité visuelle unique et soignée.',
                'price_supplement': Decimal('2000.00'),
            },
            {
                'name': 'Design Sur Mesure',
                'description': 'Design 100% personnalisé selon votre charte graphique. Création graphique complète, maquettes détaillées, révisions illimitées.',
                'price_supplement': Decimal('3500.00'),
            },
        ]

        design_options = {}
        for do_data in design_options_data:
            do, created = DesignOption.objects.update_or_create(
                name=do_data['name'],
                defaults=do_data
            )
            design_options[do_data['name']] = do
            action = "créée" if created else "mise à jour"
            self.stdout.write(f'  ✓ Option de design "{do.name}" {action}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(design_options_data)} options de design synchronisées\n'))

        # 4. Créer les Niveaux de Complexité
        complexity_levels_data = [
            {
                'name': 'Basique',
                'description': 'Fonctionnalités standards et simples. Parfait pour un site basique avec peu d\'interactions.',
                'price_multiplier': Decimal('1.00'),
            },
            {
                'name': 'Intermédiaire',
                'description': 'Fonctionnalités avancées et interactions complexes. Intégrations API, espace membre, formulaires avancés.',
                'price_multiplier': Decimal('1.50'),
            },
            {
                'name': 'Avancé',
                'description': 'Fonctionnalités très complexes et personnalisées. Développement sur mesure, logique métier complexe, intégrations multiples.',
                'price_multiplier': Decimal('2.00'),
            },
            {
                'name': 'Expert',
                'description': 'Projet hautement complexe nécessitant expertise technique pointue. Architecture avancée, scalabilité, haute performance.',
                'price_multiplier': Decimal('2.50'),
            },
        ]

        complexity_levels = {}
        for cl_data in complexity_levels_data:
            cl, created = ComplexityLevel.objects.update_or_create(
                name=cl_data['name'],
                defaults=cl_data
            )
            complexity_levels[cl_data['name']] = cl
            action = "créé" if created else "mis à jour"
            self.stdout.write(f'  ✓ Niveau de complexité "{cl.name}" {action}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(complexity_levels_data)} niveaux de complexité synchronisés\n'))

        # 5. Créer les Options Supplémentaires
        supplementary_options_data = [
            {
                'name': 'Optimisation SEO',
                'description': 'Optimisation complète pour les moteurs de recherche : meta tags, sitemap, robots.txt, schema markup, performance.',
                'price': Decimal('500.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Référencement SEO Avancé',
                'description': 'Stratégie SEO complète : audit SEO, recherche de mots-clés, optimisation technique, netlinking, suivi mensuel.',
                'price': Decimal('300.00'),
                'billing_type': 'monthly',
            },
            {
                'name': 'Maintenance Basique',
                'description': 'Mises à jour de sécurité, sauvegardes mensuelles, support par email (réponse 48h), 2h de modifications/mois.',
                'price': Decimal('80.00'),
                'billing_type': 'monthly',
            },
            {
                'name': 'Maintenance Premium',
                'description': 'Maintenance complète : mises à jour, sauvegardes hebdomadaires, support prioritaire (24h), 5h de modifications/mois, monitoring.',
                'price': Decimal('200.00'),
                'billing_type': 'monthly',
            },
            {
                'name': 'Formation',
                'description': 'Formation complète à l\'utilisation de votre site : gestion du contenu, produits, commandes. Documentation personnalisée incluse.',
                'price': Decimal('400.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Rédaction de contenu',
                'description': 'Rédaction professionnelle du contenu de votre site : pages principales, descriptions produits, articles de blog.',
                'price': Decimal('600.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Photographie professionnelle',
                'description': 'Séance photo professionnelle pour votre site : produits, locaux, équipe. Retouche et optimisation incluses.',
                'price': Decimal('800.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Création de logo',
                'description': 'Design de logo professionnel : 3 propositions, 2 révisions, fichiers dans tous les formats (AI, PNG, SVG, PDF).',
                'price': Decimal('450.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Charte graphique complète',
                'description': 'Identité visuelle complète : logo, typographies, couleurs, déclinaisons, guide d\'utilisation. Fichiers sources inclus.',
                'price': Decimal('1200.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Hébergement Standard',
                'description': 'Hébergement web performant : SSL, sauvegardes quotidiennes, certificat SSL, 20 Go stockage, bande passante illimitée.',
                'price': Decimal('15.00'),
                'billing_type': 'monthly',
            },
            {
                'name': 'Hébergement Premium',
                'description': 'Hébergement haute performance : serveur dédié, CDN, SSL premium, 100 Go stockage, monitoring 24/7, backups temps réel.',
                'price': Decimal('50.00'),
                'billing_type': 'monthly',
            },
            {
                'name': 'Nom de domaine',
                'description': 'Réservation et gestion de votre nom de domaine (.com, .fr, .net, etc.). Renouvellement automatique.',
                'price': Decimal('15.00'),
                'billing_type': 'yearly',
            },
            {
                'name': 'Certificat SSL Premium',
                'description': 'Certificat SSL premium avec validation étendue (EV) pour sécurité maximale et confiance clients.',
                'price': Decimal('200.00'),
                'billing_type': 'yearly',
            },
            {
                'name': 'Analytics et Reporting',
                'description': 'Configuration Google Analytics, tableaux de bord personnalisés, rapports mensuels détaillés sur le trafic et conversions.',
                'price': Decimal('300.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Intégration Newsletter',
                'description': 'Intégration MailChimp/Sendinblue : formulaires d\'inscription, automatisations, templates emails personnalisés.',
                'price': Decimal('400.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Espace Membre',
                'description': 'Système complet d\'authentification : inscription, connexion, profil utilisateur, mot de passe oublié.',
                'price': Decimal('800.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Multilingue',
                'description': 'Site multilingue avec traduction de tous les contenus. 2 langues incluses (langues supplémentaires : +300€/langue).',
                'price': Decimal('1000.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Application Mobile',
                'description': 'Application mobile iOS et Android native ou hybride (React Native/Flutter) connectée à votre site web.',
                'price': Decimal('5000.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Intégration CRM',
                'description': 'Connexion avec votre CRM (Salesforce, HubSpot, Pipedrive) pour synchronisation automatique des contacts et leads.',
                'price': Decimal('1500.00'),
                'billing_type': 'one_time',
            },
            {
                'name': 'Support Prioritaire',
                'description': 'Support client prioritaire : réponse garantie sous 4h en semaine, hotline téléphonique, résolution rapide des incidents.',
                'price': Decimal('150.00'),
                'billing_type': 'monthly',
            },
        ]

        supplementary_options = {}
        for so_data in supplementary_options_data:
            so, created = SupplementaryOption.objects.update_or_create(
                name=so_data['name'],
                defaults=so_data
            )
            supplementary_options[so_data['name']] = so
            action = "créée" if created else "mise à jour"
            self.stdout.write(f'  ✓ Option supplémentaire "{so.name}" {action}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(supplementary_options_data)} options supplémentaires synchronisées\n'))

        # 6. Créer les Templates de Devis (optionnel)
        templates_data = [
            {
                'name': 'Site Vitrine Standard',
                'description': 'Template pour site vitrine classique PME',
                'project_type': 'Site Vitrine',
                'design_option': 'Design Moderne',
                'complexity_level': 'Basique',
                'supplementary_options': ['Optimisation SEO', 'Formation', 'Hébergement Standard', 'Nom de domaine'],
                'default_description': '''Site vitrine professionnel pour présenter votre entreprise.

**Inclus dans ce devis :**
- Page d'accueil attractive
- Page de présentation de vos services
- Page "À propos"
- Page contact avec formulaire
- Design responsive (mobile, tablette, desktop)
- Optimisation des performances
- Formulaire de contact
- Intégration réseaux sociaux

**Livrables :**
- Site web complet et fonctionnel
- Code source
- Documentation technique
- Formation à l'administration
''',
            },
            {
                'name': 'E-commerce Complet',
                'description': 'Template pour boutique en ligne complète',
                'project_type': 'E-commerce',
                'design_option': 'Design Premium',
                'complexity_level': 'Intermédiaire',
                'supplementary_options': ['Optimisation SEO', 'Maintenance Premium', 'Formation', 'Hébergement Premium', 'Analytics et Reporting'],
                'default_description': '''Boutique en ligne complète pour vendre vos produits.

**Fonctionnalités e-commerce :**
- Catalogue produits avec recherche et filtres
- Panier d'achat intelligent
- Paiement sécurisé (Stripe, PayPal)
- Gestion des stocks automatique
- Espace client
- Suivi des commandes
- Système de promotions
- Emails transactionnels

**Administration :**
- Dashboard complet
- Gestion produits
- Gestion commandes
- Statistiques de vente
- Gestion clients

**Livrables :**
- Boutique en ligne complète
- Dashboard administrateur
- Documentation complète
- Formation approfondie
''',
            },
            {
                'name': 'Landing Page Marketing',
                'description': 'Template pour page de destination conversion',
                'project_type': 'Landing Page',
                'design_option': 'Design Moderne',
                'complexity_level': 'Basique',
                'supplementary_options': ['Optimisation SEO', 'Analytics et Reporting', 'Intégration Newsletter'],
                'default_description': '''Landing page optimisée pour maximiser vos conversions.

**Sections incluses :**
- Hero section percutante
- Proposition de valeur claire
- Bénéfices produit/service
- Témoignages clients
- Call-to-action optimisé
- Formulaire de capture
- FAQ

**Optimisations :**
- A/B testing ready
- Analytics intégrés
- Temps de chargement optimisé
- Mobile-first
- SEO optimisé

**Livrables :**
- Landing page complète
- Intégrations marketing
- Documentation
''',
            },
            {
                'name': 'Application Web Sur Mesure',
                'description': 'Template pour application web personnalisée',
                'project_type': 'Application Web',
                'design_option': 'Design Sur Mesure',
                'complexity_level': 'Avancé',
                'supplementary_options': ['Maintenance Premium', 'Formation', 'Support Prioritaire', 'Hébergement Premium'],
                'default_description': '''Application web sur mesure répondant à vos besoins spécifiques.

**Phase de conception :**
- Analyse détaillée de vos besoins
- Maquettes UX/UI complètes
- Architecture technique
- Planning détaillé

**Développement :**
- Backend robuste et scalable
- Interface utilisateur intuitive
- API REST sécurisée
- Tests automatisés
- Documentation technique

**Fonctionnalités standards :**
- Authentification multi-niveaux
- Dashboard personnalisé
- Gestion des données
- Exports et rapports
- Notifications

**Livrables :**
- Application complète
- Code source documenté
- Tests et documentation
- Formation équipe
- Maintenance assurée
''',
            },
        ]

        for tpl_data in templates_data:
            # Extraire les options supplémentaires
            supp_opt_names = tpl_data.pop('supplementary_options')

            # Remplacer les noms par les objets
            tpl_data['project_type'] = project_types[tpl_data['project_type']]
            tpl_data['design_option'] = design_options[tpl_data['design_option']]
            tpl_data['complexity_level'] = complexity_levels[tpl_data['complexity_level']]

            # Créer/Mettre à jour le template
            template, created = QuoteTemplate.objects.update_or_create(
                name=tpl_data['name'],
                defaults=tpl_data
            )

            # Associer les options supplémentaires
            template.supplementary_options.set([supplementary_options[name] for name in supp_opt_names])

            action = "créé" if created else "mis à jour"
            self.stdout.write(f'  ✓ Template "{template.name}" {action}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(templates_data)} templates de devis synchronisés\n'))

        # Résumé final
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('🎉 BASE DE DONNÉES QUOTES PEUPLÉE AVEC SUCCÈS !'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f'\n📊 Résumé :')
        self.stdout.write(f'   • 1 entreprise configurée')
        self.stdout.write(f'   • {ProjectType.objects.count()} types de projets')
        self.stdout.write(f'   • {DesignOption.objects.count()} options de design')
        self.stdout.write(f'   • {ComplexityLevel.objects.count()} niveaux de complexité')
        self.stdout.write(f'   • {SupplementaryOption.objects.count()} options supplémentaires')
        self.stdout.write(f'   • {QuoteTemplate.objects.count()} templates de devis')
        self.stdout.write(f'\n📝 Prochaines étapes :')
        self.stdout.write('   1. Testez la création de devis via l\'API ou l\'admin')
        self.stdout.write('   2. Accédez à l\'admin : http://localhost:8000/admin')
        self.stdout.write('   3. Personnalisez les options selon vos besoins\n')
