from django.contrib import admin
from review.models import Ticket, Review


class ReviewTabularInline(admin.TabularInline):
    model = Review
    extra = 0
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class TicketAdmin(admin.ModelAdmin):
    list_filter = ('title', 'created_at')
    search_fields = ['title', 'creator__username']
    ordering = ['-created_at']
    list_per_page = 20
    inlines = [ReviewTabularInline]


class CustomAdminSite(admin.AdminSite):
    site_header = "Administration de votre projet"
    site_title = "Administration du site"
    index_title = "Bienvenue sur l'interface d'administration"
    site_url = "/flux/"  # URL pour le bouton "Voir le site"


custom_admin_site = CustomAdminSite(name="custom_admin")
custom_admin_site.register(Ticket, TicketAdmin)
custom_admin_site.register(Review)


admin.site = custom_admin_site
