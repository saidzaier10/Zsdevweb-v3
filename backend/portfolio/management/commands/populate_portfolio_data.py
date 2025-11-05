"""
Commande Django pour initialiser et peupler la base de données Portfolio avec des données de démonstration.

Cette commande permet de :
- Créer les technologies utilisées (Python, Django, Vue.js, React, etc.)
- Ajouter des projets de portfolio avec descriptions détaillées
- Associer les technologies aux projets
- Créer des témoignages clients pour chaque projet

Usage:
    python manage.py populate_portfolio_data

Note: Cette commande peut être exécutée plusieurs fois (idempotente).
"""
from django.core.management.base import BaseCommand
from portfolio.models import Technology, Project, ProjectImage, Testimonial
from django.utils.text import slugify
from datetime import date


class Command(BaseCommand):
    help = 'Peuple la base de données avec des données de test pour le Portfolio'

    def handle(self, *args, **kwargs):
        """
        Point d'entrée principal de la commande.

        Processus :
        1. Création des technologies (frontend, backend, database, devops)
        2. Création des projets portfolio avec leurs détails
        3. Association des technologies aux projets (ManyToMany)
        4. Ajout des témoignages clients pour chaque projet
        """
        self.stdout.write(self.style.SUCCESS('🚀 Début du peuplement de la base de données Portfolio...'))

        # === ÉTAPE 1 : Création des Technologies ===
        # Technologies organisées par catégorie : frontend, backend, database, devops
        technologies_data = [
            {'name': 'Python', 'icon': 'devicon-python-plain', 'category': 'backend'},
            {'name': 'Django', 'icon': 'devicon-django-plain', 'category': 'backend'},
            {'name': 'Vue.js', 'icon': 'devicon-vuejs-plain', 'category': 'frontend'},
            {'name': 'React', 'icon': 'devicon-react-original', 'category': 'frontend'},
            {'name': 'JavaScript', 'icon': 'devicon-javascript-plain', 'category': 'frontend'},
            {'name': 'TypeScript', 'icon': 'devicon-typescript-plain', 'category': 'frontend'},
            {'name': 'Tailwind CSS', 'icon': 'devicon-tailwindcss-plain', 'category': 'frontend'},
            {'name': 'PostgreSQL', 'icon': 'devicon-postgresql-plain', 'category': 'database'},
            {'name': 'MongoDB', 'icon': 'devicon-mongodb-plain', 'category': 'database'},
            {'name': 'Docker', 'icon': 'devicon-docker-plain', 'category': 'devops'},
            {'name': 'Git', 'icon': 'devicon-git-plain', 'category': 'devops'},
            {'name': 'Node.js', 'icon': 'devicon-nodejs-plain', 'category': 'backend'},
        ]
        
        # Création/mise à jour des technologies (opération idempotente)
        technologies = {}
        for tech_data in technologies_data:
            tech, created = Technology.objects.update_or_create(
                name=tech_data['name'],
                defaults=tech_data
            )
            technologies[tech_data['name']] = tech
            action = "créée" if created else "mise à jour"
            self.stdout.write(f'  ✓ Technologie "{tech.name}" {action}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(technologies_data)} technologies synchronisées\n'))

        # === ÉTAPE 2 : Création des Projets Portfolio ===
        # Chaque projet contient : titre, description, technologies utilisées, URLs, dates
        projects_data = [
            {
                'title': 'Site E-commerce de Mode',
                'slug': 'site-ecommerce-mode',
                'short_description': 'Boutique en ligne complète pour une marque de vêtements avec paiement sécurisé',
                'description': '''Développement d'une plateforme e-commerce complète pour une marque de vêtements moderne.
                
**Fonctionnalités principales :**
- Catalogue produits avec filtres avancés
- Panier d'achat et wishlist
- Paiement sécurisé (Stripe, PayPal)
- Gestion des stocks en temps réel
- Espace client personnalisé
- Dashboard administrateur
- Système de promotions et codes promo
- Emails transactionnels automatiques

**Technologies utilisées :**
Backend Django REST Framework, Frontend Vue.js 3, Base de données PostgreSQL, Paiement Stripe API

**Résultats :**
- +150% de ventes en ligne
- 500+ commandes/mois
- Taux de conversion de 3.2%''',
                'technologies': ['Python', 'Django', 'Vue.js', 'PostgreSQL', 'Tailwind CSS', 'Docker'],
                'github_url': 'https://github.com/zsdevweb/ecommerce-mode',
                'live_url': 'https://demo-ecommerce.zsdevweb.com',
                'featured': True,
                'order': 1,
                'completion_date': date(2024, 10, 15),
            },
            {
                'title': 'Application de Gestion RH',
                'slug': 'application-gestion-rh',
                'short_description': 'Système complet de gestion des ressources humaines pour PME',
                'description': '''Application web sur mesure pour la gestion complète des RH d'une entreprise de 50+ employés.

**Fonctionnalités :**
- Gestion des employés et organigramme
- Gestion des congés et absences
- Suivi des performances
- Gestion de la paie
- Tableau de bord RH
- Notifications automatiques
- Exports et rapports

**Stack technique :**
Django, React, PostgreSQL, Celery pour les tâches asynchrones, Redis pour le cache

**Impact :**
- -60% de temps administratif
- Digitalisation complète des processus RH
- Satisfaction employés : 4.8/5''',
                'technologies': ['Python', 'Django', 'React', 'PostgreSQL', 'Docker'],
                'github_url': 'https://github.com/zsdevweb/gestion-rh',
                'live_url': '',
                'featured': True,
                'order': 2,
                'completion_date': date(2024, 9, 20),
            },
            {
                'title': 'Portfolio Photographe',
                'slug': 'portfolio-photographe',
                'short_description': 'Site portfolio élégant pour photographe professionnel avec galerie interactive',
                'description': '''Site portfolio moderne et épuré pour un photographe professionnel.

**Caractéristiques :**
- Galerie photos avec lightbox
- Catégorisation des projets
- Page À propos
- Formulaire de contact
- Blog intégré
- Optimisation images
- SEO optimisé

**Technologies :**
Vue.js 3, Vite, Tailwind CSS, Backend Django pour le blog

**Résultats :**
- Design minimaliste et élégant
- Temps de chargement < 1s
- Score Google Lighthouse : 98/100''',
                'technologies': ['Vue.js', 'Django', 'Tailwind CSS', 'PostgreSQL'],
                'github_url': '',
                'live_url': 'https://photographe-demo.zsdevweb.com',
                'featured': True,
                'order': 3,
                'completion_date': date(2024, 8, 10),
            },
            {
                'title': 'API REST pour Application Mobile',
                'slug': 'api-rest-mobile',
                'short_description': 'API backend robuste pour application de livraison de repas',
                'description': '''Backend complet pour une application mobile de livraison de repas.

**Services développés :**
- Authentification JWT
- Gestion des restaurants
- Système de commandes
- Géolocalisation
- Paiements en ligne
- Notifications push
- Dashboard analytics

**Stack :**
Django REST Framework, PostgreSQL, Redis, Celery, AWS S3

**Performance :**
- 10,000+ requêtes/jour
- Temps de réponse moyen : 120ms
- Disponibilité : 99.9%''',
                'technologies': ['Python', 'Django', 'PostgreSQL', 'Docker', 'Git'],
                'github_url': 'https://github.com/zsdevweb/food-delivery-api',
                'live_url': '',
                'featured': False,
                'order': 4,
                'completion_date': date(2024, 7, 5),
            },
            {
                'title': 'Dashboard Analytics SaaS',
                'slug': 'dashboard-analytics-saas',
                'short_description': 'Plateforme SaaS de visualisation de données en temps réel',
                'description': '''Plateforme SaaS complète pour la visualisation et l'analyse de données business.

**Fonctionnalités :**
- Tableaux de bord personnalisables
- Graphiques interactifs
- Rapports automatisés
- Exports PDF/Excel
- Alertes personnalisées
- Multi-utilisateurs
- API publique

**Technologies :**
Vue.js 3, Django, PostgreSQL, Chart.js, WebSockets pour temps réel

**Metrics :**
- 30+ clients entreprises
- 500GB+ données analysées/mois
- Interface intuitive et moderne''',
                'technologies': ['Vue.js', 'Django', 'PostgreSQL', 'Docker', 'JavaScript'],
                'github_url': '',
                'live_url': 'https://analytics.zsdevweb.com',
                'featured': False,
                'order': 5,
                'completion_date': date(2024, 6, 18),
            },
            {
                'title': 'Site Institutionnel',
                'slug': 'site-institutionnel',
                'short_description': 'Site web corporate pour cabinet d\'avocats avec espace client sécurisé',
                'description': '''Site web professionnel pour cabinet d'avocats avec espace client.

**Sections :**
- Présentation du cabinet
- Équipe d'avocats
- Domaines d'expertise
- Actualités juridiques
- Espace client sécurisé
- Prise de rendez-vous en ligne
- Formulaires confidentiels

**Stack technique :**
Django, Tailwind CSS, PostgreSQL, Authentification sécurisée

**Résultats :**
- Design professionnel et rassurant
- +40% de demandes de consultation
- Conformité RGPD''',
                'technologies': ['Python', 'Django', 'Tailwind CSS', 'PostgreSQL'],
                'github_url': '',
                'live_url': 'https://cabinet-demo.zsdevweb.com',
                'featured': False,
                'order': 6,
                'completion_date': date(2024, 5, 12),
            },
        ]
        
        # Traitement des projets avec association des technologies
        projects = {}
        for proj_data in projects_data:
            # Extraire les noms de technologies pour traitement séparé (relation ManyToMany)
            tech_names = proj_data.pop('technologies')

            # Création/mise à jour du projet (idempotent via slug unique)
            project, created = Project.objects.update_or_create(
                slug=proj_data['slug'],
                defaults=proj_data
            )

            # Association des technologies au projet (relation ManyToMany)
            # set() remplace toutes les associations existantes
            project.technologies.set([technologies[name] for name in tech_names])
            
            projects[proj_data['slug']] = project
            action = "créé" if created else "mis à jour"
            self.stdout.write(f'  ✓ Projet "{project.title}" {action}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(projects_data)} projets synchronisés\n'))

        # === ÉTAPE 3 : Création des Témoignages Clients ===
        # Témoignages associés à chaque projet pour crédibilité et social proof
        testimonials_data = [
            {
                'client_name': 'Sophie Martin',
                'client_position': 'CEO',
                'client_company': 'Mode & Style',
                'content': 'ZSdevweb a créé notre boutique en ligne de A à Z. Le résultat dépasse nos attentes ! Site moderne, rapide et facile à utiliser. Nos ventes ont explosé.',
                'rating': 5,
                'project': 'site-ecommerce-mode',
            },
            {
                'client_name': 'Thomas Dubois',
                'client_position': 'Photographe Professionnel',
                'client_company': 'Thomas Dubois Photography',
                'content': 'Un portfolio qui met parfaitement en valeur mon travail. Design épuré, navigation fluide. Mes clients adorent ! Service professionnel et réactif.',
                'rating': 5,
                'project': 'portfolio-photographe',
            },
            {
                'client_name': 'Marie Lefebvre',
                'client_position': 'DRH',
                'client_company': 'InnovTech Solutions',
                'content': 'L\'application RH a transformé notre gestion quotidienne. Tout est digitalisé et automatisé. Un gain de temps énorme et nos employés sont ravis.',
                'rating': 5,
                'project': 'application-gestion-rh',
            },
            {
                'client_name': 'Pierre Rousseau',
                'client_position': 'Fondateur',
                'client_company': 'FastFood Delivery',
                'content': 'API robuste et performante qui supporte notre croissance. Support technique excellent. ZSdevweb comprend vraiment les besoins techniques.',
                'rating': 5,
                'project': 'api-rest-mobile',
            },
            {
                'client_name': 'Julie Bernard',
                'client_position': 'Associée',
                'client_company': 'Cabinet Bernard & Associés',
                'content': 'Site professionnel et sécurisé, parfait pour notre cabinet. L\'espace client facilite nos échanges avec nos clients. Très satisfaits du résultat.',
                'rating': 5,
                'project': 'site-institutionnel',
            },
            {
                'client_name': 'Lucas Petit',
                'client_position': 'CTO',
                'client_company': 'DataViz Pro',
                'content': 'Dashboard analytics puissant et intuitif. Nos clients apprécient l\'interface moderne et les fonctionnalités avancées. Excellent travail !',
                'rating': 5,
                'project': 'dashboard-analytics-saas',
            },
        ]
        
        # Association des témoignages aux projets
        for test_data in testimonials_data:
            # Conversion du slug de projet en objet Project (foreign key)
            project_slug = test_data.pop('project')
            test_data['project'] = projects[project_slug]

            # Création/mise à jour du témoignage (idempotent via client_name)
            testimonial, created = Testimonial.objects.update_or_create(
                client_name=test_data['client_name'],
                defaults=test_data
            )
            action = "créé" if created else "mis à jour"
            self.stdout.write(f'  ✓ Témoignage de "{testimonial.client_name}" {action}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(testimonials_data)} témoignages synchronisés\n'))

        # === Résumé final de l'exécution ===
        # Affichage récapitulatif des données créées
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('🎉 BASE DE DONNÉES PORTFOLIO PEUPLÉE AVEC SUCCÈS !'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f'\n📊 Résumé de l\'initialisation :')
        self.stdout.write(f'   • {Technology.objects.count()} technologies')
        self.stdout.write(f'   • {Project.objects.count()} projets')
        self.stdout.write(f'   • {Testimonial.objects.count()} témoignages\n')