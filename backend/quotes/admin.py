from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from .models import (
    Company,
    ProjectCategory,
    ProjectType,
    DesignOption,
    ComplexityLevel,
    SupplementaryOption,
    QuoteTemplate,
    Quote,
    QuoteEmailLog
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Administration des informations de l'entreprise"""
    
    fieldsets = (
        ('🏢 Informations générales', {
            'fields': ('name', 'logo', 'email', 'phone', 'address')
        }),
        ('📋 Informations légales', {
            'fields': ('siret', 'tva_number')
        }),
        ('🎨 Personnalisation PDF', {
            'fields': ('primary_color', 'footer_text')
        }),
        ('✉️ Configuration emails', {
            'fields': ('email_signature',)
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        """Empêcher la création de plusieurs entreprises"""
        return not Company.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Empêcher la suppression"""
        return False


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    """Administration des catégories de projets"""
    list_display = ['name', 'slug', 'display_color', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('📋 Informations', {
            'fields': ('name', 'slug', 'description')
        }),
        ('🎨 Présentation', {
            'fields': ('icon', 'color', 'order')
        }),
        ('⚙️ Paramètres', {
            'fields': ('is_active',)
        }),
    )

    def display_color(self, obj):
        """Affiche un aperçu de la couleur"""
        return format_html(
            '<span style="background-color: {}; padding: 5px 15px; color: white; border-radius: 4px;">●</span>',
            obj.color
        )
    display_color.short_description = 'Couleur'


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'base_price', 'estimated_days', 'is_active', 'created_at']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(DesignOption)
class DesignOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_supplement', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(ComplexityLevel)
class ComplexityLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_multiplier', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(SupplementaryOption)
class SupplementaryOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'billing_type', 'display_categories', 'is_active', 'created_at']
    list_filter = ['is_active', 'billing_type', 'compatible_categories']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    filter_horizontal = ['compatible_categories']

    fieldsets = (
        ('📋 Informations', {
            'fields': ('name', 'description')
        }),
        ('💰 Tarification', {
            'fields': ('price', 'billing_type')
        }),
        ('🔧 Compatibilité', {
            'fields': ('compatible_categories',),
            'description': 'Laissez vide pour rendre l\'option disponible pour toutes les catégories'
        }),
        ('⚙️ Paramètres', {
            'fields': ('is_active',)
        }),
    )

    def display_categories(self, obj):
        """Affiche les catégories compatibles"""
        categories = obj.compatible_categories.all()
        if not categories.exists():
            return format_html('<span style="color: #10b981;">✓ Toutes catégories</span>')
        return format_html(
            '<span>{}</span>',
            ', '.join([cat.name for cat in categories])
        )
    display_categories.short_description = 'Catégories'


@admin.register(QuoteTemplate)
class QuoteTemplateAdmin(admin.ModelAdmin):
    """Administration des templates de devis"""
    
    list_display = ['name', 'project_type', 'design_option', 'complexity_level', 'is_active', 'created_at']
    list_filter = ['is_active', 'project_type', 'design_option']
    search_fields = ['name', 'description', 'default_description']
    filter_horizontal = ['supplementary_options']
    list_editable = ['is_active']
    
    fieldsets = (
        ('📋 Informations du template', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('⚙️ Configuration par défaut', {
            'fields': ('project_type', 'design_option', 'complexity_level', 'supplementary_options')
        }),
        ('📝 Texte par défaut', {
            'fields': ('default_description',)
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


class QuoteEmailLogInline(admin.TabularInline):
    """Inline pour voir les emails envoyés"""
    model = QuoteEmailLog
    extra = 0
    readonly_fields = ['email_type', 'recipient', 'subject', 'sent_at', 'success', 'error_message']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """Administration des devis avec toutes les fonctionnalités Premium"""
    
    list_display = [
        'quote_number',
        'display_status',
        'client_name',
        'client_email',
        'project_type',
        'display_total',
        'display_discount',
        'display_signature',
        'created_at'
    ]
    
    list_filter = [
        'status',
        'project_type',
        'design_option',
        'complexity_level',
        'created_at',
        'assigned_to'
    ]
    
    search_fields = [
        'quote_number',
        'client_name',
        'client_email',
        'company_name',
        'project_description',
        'internal_notes'
    ]
    
    readonly_fields = [
        'quote_number',
        'subtotal_ht',
        'discount_amount',
        'tva_amount',
        'total_ttc',
        'payment_first',
        'payment_second',
        'payment_final',
        'estimated_duration_days',
        'estimated_end_date',
        'signature_token',
        'display_signature_url',
        'created_at',
        'updated_at',
        'sent_at',
        'viewed_at',
        'accepted_at',
        'rejected_at',
        'signed_at',
        'expires_at',
        'display_is_expired'
    ]
    
    filter_horizontal = ['supplementary_options']
    date_hierarchy = 'created_at'
    inlines = [QuoteEmailLogInline]
    
    fieldsets = (
        ('📋 Informations du devis', {
            'fields': (
                'quote_number',
                'status',
                'template',
                'assigned_to',
                'expires_at',
                'display_is_expired'
            )
        }),
        ('👤 Informations client', {
            'fields': (
                'client_name',
                'client_email',
                'client_phone',
                'company_name',
                'client_address'
            )
        }),
        ('🔧 Configuration du projet', {
            'fields': (
                'project_type',
                'design_option',
                'complexity_level',
                'supplementary_options'
            )
        }),
        ('📝 Détails du projet', {
            'fields': (
                'project_description',
                'deadline',
                'estimated_start_date',
                'estimated_duration_days',
                'estimated_end_date'
            )
        }),
        ('💰 Calculs financiers', {
            'fields': (
                'tva_rate',
                'subtotal_ht',
                ('discount_type', 'discount_value'),
                'discount_reason',
                'discount_amount',
                'tva_amount',
                'total_ttc'
            ),
            'description': 'Les montants sont calculés automatiquement'
        }),
        ('💳 Conditions de paiement', {
            'fields': (
                'payment_first',
                'payment_second',
                'payment_final'
            ),
            'description': 'Répartition : 30% / 40% / 30%'
        }),
        ('✍️ Signature électronique', {
            'fields': (
                'signature_token',
                'display_signature_url',
                'signature_image',
                'signed_at',
                'client_ip'
            )
        }),
        ('📄 Fichier PDF', {
            'fields': ('pdf_file',)
        }),
        ('📝 Notes internes', {
            'fields': ('internal_notes',),
            'classes': ('collapse',),
            'description': 'Visible uniquement par les administrateurs'
        }),
        ('📅 Dates et historique', {
            'fields': (
                'created_at',
                'updated_at',
                'sent_at',
                'viewed_at',
                'accepted_at',
                'rejected_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Méthodes d'affichage personnalisées
    
    def display_total(self, obj):
        """Affiche le total TTC avec formatage"""
        return format_html(
            '<strong style="color: #059669; font-size: 14px;">{} €</strong>',
            obj.total_ttc
        )
    display_total.short_description = 'Total TTC'
    
    def display_status(self, obj):
        """Affiche le statut avec une couleur"""
        colors = {
            'draft': '#6b7280',
            'sent': '#3b82f6',
            'viewed': '#8b5cf6',
            'accepted': '#10b981',
            'rejected': '#ef4444',
            'expired': '#f59e0b',
        }
        color = colors.get(obj.status, '#6b7280')
        
        # Vérifier si expiré
        is_expired = ' ⚠️' if obj.is_expired and obj.status not in ['accepted', 'rejected'] else ''
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}{}',
            color,
            obj.get_status_display(),
            is_expired
        )
    display_status.short_description = 'Statut'
    
    def display_discount(self, obj):
        """Affiche la remise"""
        if obj.discount_value > 0:
            if obj.discount_type == 'percent':
                return format_html(
                    '<span style="color: #ef4444;">-{}% (-{} €)</span>',
                    obj.discount_value,
                    obj.discount_amount
                )
            else:
                return format_html(
                    '<span style="color: #ef4444;">-{} €</span>',
                    obj.discount_amount
                )
        return '-'
    display_discount.short_description = 'Remise'
    
    def display_signature(self, obj):
        """Affiche le statut de signature"""
        if obj.signed_at:
            return format_html(
                '<span style="color: #10b981;">✓ Signé le {}</span>',
                obj.signed_at.strftime('%d/%m/%Y %H:%M')
            )
        return format_html('<span style="color: #6b7280;">Non signé</span>')
    display_signature.short_description = 'Signature'
    
    def display_signature_url(self, obj):
        """Affiche l'URL de signature"""
        if obj.signature_token:
            url = f"/api/quotes/public/{obj.signature_token}/"
            return format_html(
                '<a href="{}" target="_blank" style="color: #1a56db;">🔗 Lien public</a><br>'
                '<small style="color: #6b7280;">Token: {}</small>',
                url,
                obj.signature_token[:20] + '...'
            )
        return '-'
    display_signature_url.short_description = 'URL publique'
    
    def display_is_expired(self, obj):
        """Affiche si le devis est expiré"""
        if obj.is_expired:
            return format_html('<span style="color: #ef4444; font-weight: bold;">⚠️ EXPIRÉ</span>')
        elif obj.expires_at:
            days_left = (obj.expires_at - timezone.now()).days
            if days_left <= 3:
                return format_html(
                    '<span style="color: #f59e0b;">Expire dans {} jours</span>',
                    days_left
                )
            return format_html(
                '<span style="color: #10b981;">Valide ({} jours restants)</span>',
                days_left
            )
        return '-'
    display_is_expired.short_description = 'Validité'
    
    # Actions personnalisées
    
    actions = [
        'mark_as_sent',
        'mark_as_accepted',
        'mark_as_rejected',
    ]
    
    def mark_as_sent(self, request, queryset):
        """Marquer les devis comme envoyés"""
        updated = queryset.update(status='sent', sent_at=timezone.now())
        self.message_user(
            request,
            f'{updated} devis marqué(s) comme envoyé(s).',
            messages.SUCCESS
        )
    mark_as_sent.short_description = "📤 Marquer comme envoyé"
    
    def mark_as_accepted(self, request, queryset):
        """Marquer les devis comme acceptés"""
        updated = queryset.update(status='accepted', accepted_at=timezone.now())
        self.message_user(
            request,
            f'{updated} devis marqué(s) comme accepté(s).',
            messages.SUCCESS
        )
    mark_as_accepted.short_description = "✅ Marquer comme accepté"
    
    def mark_as_rejected(self, request, queryset):
        """Marquer les devis comme refusés"""
        updated = queryset.update(status='rejected', rejected_at=timezone.now())
        self.message_user(
            request,
            f'{updated} devis marqué(s) comme refusé(s).',
            messages.WARNING
        )
    mark_as_rejected.short_description = "❌ Marquer comme refusé"


@admin.register(QuoteEmailLog)
class QuoteEmailLogAdmin(admin.ModelAdmin):
    """Administration des logs d'emails"""
    
    list_display = [
        'quote',
        'email_type',
        'recipient',
        'subject',
        'sent_at',
        'display_success'
    ]
    
    list_filter = ['email_type', 'success', 'sent_at']
    search_fields = ['recipient', 'subject', 'error_message']
    readonly_fields = ['quote', 'email_type', 'recipient', 'subject', 'sent_at', 'success', 'error_message']
    date_hierarchy = 'sent_at'
    
    def display_success(self, obj):
        """Affiche le statut d'envoi"""
        if obj.success:
            return format_html('<span style="color: #10b981;">✓ Envoyé</span>')
        return format_html(
            '<span style="color: #ef4444;">✗ Échec</span><br><small>{}</small>',
            obj.error_message[:50]
        )
    display_success.short_description = 'Statut'
    
    def has_add_permission(self, request):
        """Empêcher la création manuelle"""
        return False