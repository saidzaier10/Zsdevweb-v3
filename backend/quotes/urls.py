from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectCategoryViewSet,
    ProjectTypeViewSet,
    DesignOptionViewSet,
    ComplexityLevelViewSet,
    SupplementaryOptionViewSet,
    QuoteViewSet
)

router = DefaultRouter()
router.register(r'categories', ProjectCategoryViewSet, basename='projectcategory')
router.register(r'project-types', ProjectTypeViewSet, basename='projecttype')
router.register(r'design-options', DesignOptionViewSet, basename='designoption')
router.register(r'complexity-levels', ComplexityLevelViewSet, basename='complexitylevel')
router.register(r'supplementary-options', SupplementaryOptionViewSet, basename='supplementaryoption')
router.register(r'quotes', QuoteViewSet, basename='quote')

urlpatterns = [
    path('', include(router.urls)),
]