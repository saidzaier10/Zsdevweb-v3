from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TechnologyViewSet, ProjectViewSet, TestimonialViewSet, ContactMessageViewSet, statistics

router = DefaultRouter()
router.register(r'technologies', TechnologyViewSet, basename='technology')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'contact', ContactMessageViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', statistics, name='portfolio-statistics'),
]