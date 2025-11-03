from rest_framework import serializers
from .models import Technology, Project, ProjectImage, Testimonial


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'name', 'icon', 'category', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'order', 'created_at']
        read_only_fields = ['created_at']


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des projets (moins de détails)"""
    technologies = TechnologySerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    # Aliases pour compatibilité frontend
    description = serializers.CharField(source='short_description', read_only=True)
    image = serializers.ImageField(source='thumbnail', read_only=True)
    url = serializers.URLField(source='live_url', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'description',
            'thumbnail', 'image', 'technologies', 'category', 'category_display',
            'url', 'live_url', 'featured', 'order', 'completion_date'
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer pour le détail d'un projet (toutes les infos)"""
    technologies = TechnologySerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    testimonials = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'description',
            'thumbnail', 'image_main', 'technologies', 'images',
            'github_url', 'live_url', 'category', 'category_display',
            'featured', 'order', 'is_published',
            'completion_date', 'created_at', 'updated_at', 'testimonials'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_testimonials(self, obj):
        testimonials = obj.testimonials.filter(is_published=True)
        return TestimonialSerializer(testimonials, many=True).data


class TestimonialSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = Testimonial
        fields = [
            'id', 'client_name', 'client_position', 'client_company',
            'client_photo', 'content', 'rating', 'project', 'project_title',
            'is_published', 'order', 'created_at'
        ]
        read_only_fields = ['created_at']