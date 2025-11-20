#!/usr/bin/env python
"""
Script de test pour vérifier que tous les imports du refactoring fonctionnent
"""
import sys
import os

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zsdevweb.settings')

try:
    import django
    django.setup()
    print("✅ Django configuré")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

# Test 1: Import des constantes
print("\n=== Test 1: Import des constantes ===")
try:
    from quotes.utils import (
        QuoteStatus,
        BillingType,
        DiscountType,
        EmailType,
        PaymentConfig,
        QuoteConfig,
        FileExtensions,
        ErrorMessages,
        SuccessMessages,
        ValidationLimits,
    )
    print("✅ Toutes les constantes importées")
    print(f"   - QuoteStatus.DRAFT = {QuoteStatus.DRAFT}")
    print(f"   - ErrorMessages.QUOTE_ALREADY_SIGNED = {ErrorMessages.QUOTE_ALREADY_SIGNED}")
except Exception as e:
    print(f"❌ Erreur import constantes: {e}")

# Test 2: Import du validateur
print("\n=== Test 2: Import du validateur ===")
try:
    from quotes.utils import QuoteValidator
    print("✅ QuoteValidator importé")
    print(f"   - Type: {type(QuoteValidator)}")
except Exception as e:
    print(f"❌ Erreur import QuoteValidator: {e}")

# Test 3: Import des décorateurs
print("\n=== Test 3: Import des décorateurs ===")
try:
    from quotes.utils import handle_service_errors, log_quote_action
    print("✅ Décorateurs importés")
    print(f"   - handle_service_errors: {type(handle_service_errors)}")
    print(f"   - log_quote_action: {type(log_quote_action)}")
except Exception as e:
    print(f"❌ Erreur import décorateurs: {e}")

# Test 4: Import des services
print("\n=== Test 4: Import des services ===")
try:
    from quotes.services import (
        PDFService,
        SignatureService,
        EmailService,
        QuoteService,
    )
    print("✅ Tous les services importés")
    print(f"   - PDFService: {type(PDFService)}")
    print(f"   - SignatureService: {type(SignatureService)}")
    print(f"   - EmailService: {type(EmailService)}")
    print(f"   - QuoteService: {type(QuoteService)}")
except Exception as e:
    print(f"❌ Erreur import services: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Import de views.py
print("\n=== Test 5: Import des views ===")
try:
    from quotes import views
    print("✅ quotes.views importé")
    print(f"   - QuoteViewSet: {hasattr(views, 'QuoteViewSet')}")
except Exception as e:
    print(f"❌ Erreur import views: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Vérifier que QuoteViewSet a les bonnes méthodes
print("\n=== Test 6: Vérification QuoteViewSet ===")
try:
    from quotes.views import QuoteViewSet
    methods = ['create', 'download_pdf', 'send_email', 'sign_quote', 'reject', 'duplicate']
    for method in methods:
        if hasattr(QuoteViewSet, method):
            print(f"✅ Méthode {method} présente")
        else:
            print(f"❌ Méthode {method} manquante")
except Exception as e:
    print(f"❌ Erreur vérification QuoteViewSet: {e}")

# Test 7: Test de validation simple
print("\n=== Test 7: Test de validation ===")
try:
    from quotes.utils import QuoteValidator
    is_valid, error = QuoteValidator.validate_discount('percent', 10, 1000)
    if is_valid:
        print(f"✅ Validation discount: {is_valid} (error: {error})")
    else:
        print(f"❌ Validation discount échouée: {error}")
except Exception as e:
    print(f"❌ Erreur test validation: {e}")

print("\n=== Résumé ===")
print("Si tous les tests sont ✅, le refactoring backend est correct!")
print("Si des tests sont ❌, vérifiez les erreurs ci-dessus.")
