from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CompanyViewSet,
    ProjectTypeViewSet,
    DesignOptionViewSet,
    ComplexityLevelViewSet,
    SupplementaryOptionViewSet,
    QuoteTemplateViewSet,
    QuoteViewSet,
    QuoteEmailLogViewSet,
)

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
    path('', include(router.urls)),
]