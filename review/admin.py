from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from review.models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):

    def response_change(self, request, obj):
        # Vérifier si l'objet en cours de modification est une instance de Ticket
        if isinstance(obj, Ticket):
            # Rediriger vers la vue flux après la modification du ticket
            return HttpResponseRedirect(reverse("flux"))
        return super().response_change(request, obj)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review)

