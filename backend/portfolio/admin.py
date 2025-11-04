from django.contrib import admin
from django.utils.html import format_html
from .models import Technology, Project, ProjectImage, Testimonial, ContactMessage


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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'read_at', 'replied_at', 'ip_address', 'user_agent']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Expéditeur', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Statut', {
            'fields': ('status', 'read_at', 'replied_at')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_archived']

    def status_badge(self, obj):
        """Afficher un badge coloré pour le statut"""
        colors = {
            'new': '#ef4444',  # Rouge
            'read': '#f59e0b',  # Orange
            'replied': '#10b981',  # Vert
            'archived': '#6b7280',  # Gris
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Statut'

    def mark_as_read(self, request, queryset):
        """Action pour marquer les messages comme lus"""
        for message in queryset:
            message.mark_as_read()
        self.message_user(request, f"{queryset.count()} message(s) marqué(s) comme lu(s).")
    mark_as_read.short_description = "Marquer comme lu"

    def mark_as_replied(self, request, queryset):
        """Action pour marquer les messages comme répondus"""
        for message in queryset:
            message.mark_as_replied()
        self.message_user(request, f"{queryset.count()} message(s) marqué(s) comme répondu(s).")
    mark_as_replied.short_description = "Marquer comme répondu"

    def mark_as_archived(self, request, queryset):
        """Action pour archiver les messages"""
        queryset.update(status='archived')
        self.message_user(request, f"{queryset.count()} message(s) archivé(s).")
    mark_as_archived.short_description = "Archiver"
