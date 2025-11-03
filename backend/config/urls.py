"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from quotes.views import (
    CompanyViewSet,
    ProjectTypeViewSet,
    DesignOptionViewSet,
    ComplexityLevelViewSet,
    SupplementaryOptionViewSet,
    QuoteTemplateViewSet,
    QuoteViewSet,
    QuoteEmailLogViewSet
)

# Router pour l'API
router = DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'project-types', ProjectTypeViewSet, basename='projecttype')
router.register(r'design-options', DesignOptionViewSet, basename='designoption')
router.register(r'complexity-levels', ComplexityLevelViewSet, basename='complexitylevel')
router.register(r'supplementary-options', SupplementaryOptionViewSet, basename='supplementaryoption')
router.register(r'quote-templates', QuoteTemplateViewSet, basename='quotetemplate')
router.register(r'quotes', QuoteViewSet, basename='quote')
router.register(r'quote-email-logs', QuoteEmailLogViewSet, basename='quoteemaillog')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('routers.urls')),
    path('api/auth/', include('users.urls')),
    path('api/portfolio/', include('portfolio.urls')),
]