from django.contrib import admin
from .models import Technology, Project, ProjectImage, Testimonial


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name']


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'featured', 'is_published', 'order', 'completion_date']
    list_filter = ['featured', 'is_published', 'completion_date']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    inlines = [ProjectImageInline]
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Images', {
            'fields': ('thumbnail', 'image_main')
        }),
        ('Technologies', {
            'fields': ('technologies',)
        }),
        ('Liens', {
            'fields': ('github_url', 'live_url')
        }),
        ('Paramètres', {
            'fields': ('featured', 'order', 'is_published', 'completion_date')
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'rating', 'project', 'is_published', 'created_at']
    list_filter = ['rating', 'is_published', 'created_at']
    search_fields = ['client_name', 'client_company', 'content']
