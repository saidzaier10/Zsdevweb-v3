from django.contrib import admin
from .models import ProjectType, DesignOption, ComplexityLevel, SupplementaryOption, Quote


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(DesignOption)
class DesignOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_supplement', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(ComplexityLevel)
class ComplexityLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_multiplier', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(SupplementaryOption)
class SupplementaryOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_name', 'client_email', 'project_type', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'project_type', 'design_option', 'complexity_level', 'created_at']
    search_fields = ['client_name', 'client_email', 'company_name', 'project_description']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    filter_horizontal = ['supplementary_options']
    
    fieldsets = (
        ('Informations client', {
            'fields': ('client_name', 'client_email', 'client_phone', 'company_name')
        }),
        ('Configuration du projet', {
            'fields': ('project_type', 'design_option', 'complexity_level', 'supplementary_options')
        }),
        ('Détails', {
            'fields': ('project_description', 'deadline')
        }),
        ('Prix et statut', {
            'fields': ('total_price', 'status')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )