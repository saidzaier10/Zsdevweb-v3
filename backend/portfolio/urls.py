from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TechnologyViewSet, ProjectViewSet, TestimonialViewSet

router = DefaultRouter()
router.register(r'technologies', TechnologyViewSet, basename='technology')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('', include(router.urls)),
]