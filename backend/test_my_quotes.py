#!/usr/bin/env python
"""
Script de test pour diagnostiquer le problème avec l'endpoint my-quotes
"""
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from quotes.views import QuoteViewSet
from quotes.models import Quote
from users.models import User

print("="*60)
print("TEST DE L'ENDPOINT MY-QUOTES")
print("="*60)

# 1. Vérifier l'utilisateur Arthur
print("\n1. Vérification de l'utilisateur...")
try:
    user = User.objects.get(username='Arthur')
    print(f"   ✅ Utilisateur trouvé: {user.username}")
    print(f"   📧 Email: {user.email}")
    print(f"   🔑 ID: {user.id}")
except User.DoesNotExist:
    print("   ❌ Utilisateur 'Arthur' non trouvé!")
    print("\n   Utilisateurs disponibles:")
    for u in User.objects.all():
        print(f"      - {u.username} ({u.email})")
    exit(1)

# 2. Vérifier les devis
print("\n2. Vérification des devis...")
all_quotes = Quote.objects.all()
print(f"   📊 Total devis dans la BDD: {all_quotes.count()}")

if all_quotes.count() > 0:
    print("\n   Détails des devis:")
    for quote in all_quotes:
        print(f"      - ID: {quote.id}, Client: {quote.client_name}, Email: {quote.client_email}")
        print(f"        Statut: {quote.status}, Numéro: {quote.quote_number}")
        if quote.client_email == user.email:
            print(f"        ✅ Ce devis correspond à l'email d'Arthur!")
        else:
            print(f"        ⚠️  Email différent de Arthur ({user.email})")

# 3. Tester l'endpoint my_quotes
print("\n3. Test de l'endpoint my_quotes...")

factory = APIRequestFactory()
request = factory.get('/api/quotes/quotes/my-quotes/')
force_authenticate(request, user=user)

try:
    viewset = QuoteViewSet.as_view({'get': 'my_quotes'})
    response = viewset(request)
    
    print(f"   ✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"   ✅ Nombre de devis retournés: {len(response.data)}")
        if len(response.data) > 0:
            print("\n   📋 Devis retournés:")
            for quote_data in response.data:
                print(f"      - #{quote_data.get('quote_number')} - {quote_data.get('client_name')}")
        else:
            print("\n   ⚠️  Aucun devis retourné pour cet utilisateur")
            print(f"   💡 L'email du devis doit correspondre à: {user.email}")
    else:
        print(f"   ❌ Erreur: {response.data}")
        
except AttributeError as e:
    print(f"   ❌ L'action 'my_quotes' n'existe pas dans le ViewSet!")
    print(f"   Erreur: {e}")
except Exception as e:
    print(f"   ❌ Erreur lors du test: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("FIN DU TEST")
print("="*60)