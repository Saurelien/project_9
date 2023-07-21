from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.views.generic.edit import FormView
from review.models import UserFollows
from django.shortcuts import get_object_or_404, reverse
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView  # ListView
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Ticket
from django.shortcuts import redirect

UserModel = get_user_model()

# class AbonnementView(TemplateView):
#     template_name = 'review/abonnements.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # Récupérer l'utilisateur suivi depuis la session
#         utilisateur_suivi = self.request.session.get('utilisateur_suivi')
#
#         if utilisateur_suivi:
#             # Récupérer les abonnés de l'utilisateur suivi
#             abonnes = User.objects.filter(utilisateurs_suivis__username=utilisateur_suivi)
#
#             # Récupérer les utilisateurs suivis par l'utilisateur actuel
#             utilisateurs_suivis = User.objects.filter(abonnes=self.request.user)
#
#             # Ajouter les utilisateurs suivis et les abonnés au contexte
#             context['utilisateurs_suivis'] = utilisateurs_suivis
#             context['abonnes'] = abonnes
#
#         return context

# class SearchUserView(LoginRequiredMixin, View):
#     def get(self, request):
#         data = []
#         query = request.GET.get('q')
#         if query is None or len(query) < 3:
#             return JsonResponse(data, safe=False)
#         users = User.objects.filter(username__startswith=query)
#         for user in users:
#             data.append({"id": user.pk, "username": user.username})
#
#         return JsonResponse(data, safe=False)


class FluxView(LoginRequiredMixin, TemplateView):
    template_name = 'review/flux.html'


class SearchUserView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q')
        if query and len(query) >= 3:
            users = UserModel.objects.filter(username__startswith=query)
        else:
            users = []

        context = {'users': users}
        return render(request, 'review/recherche_utilisateur.html', context)


class FollowUserForm(forms.Form):
    username = forms.CharField()


class FollowUserView(LoginRequiredMixin, FormView):
    template_name = 'review/flux_utilisateurs.html'
    form_class = FollowUserForm
    success_url = reverse_lazy('flux_utilisateurs')

    def form_valid(self, form):
        followed = UserModel.objects.filter(username=form.cleaned_data['username']).first()
        print("#" * 79)
        if followed:
            UserFollows.objects.get_or_create(follower=self.request.user, followed_user=followed)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ajouter les utilisateurs suivis et les abonnés au contexte
        context['utilisateurs_suivis'] = self.request.user.following.all()
        context['abonnes'] = self.request.user.followers.all()

        return context


""" Classe prototype pour le systeme d'abonnement utilisateur"""


class UnfollowUserView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # Récupérer l'utilisateur à ne plus suivre
        username = self.kwargs.get('username')
        followed_user = get_object_or_404(UserModel, username=username)

        # Supprimer la relation de suivi entre l'utilisateur connecté et l'utilisateur suivi
        UserFollows.objects.filter(follower=self.request.user, followed_user=followed_user).delete()

        # Rediriger l'utilisateur vers une page appropriée (par exemple, le profil de l'utilisateur suivi)
        return reverse('user_profile', kwargs={'username': username})


""" Vue de la gestion des tickets """
""" Consommation du model Ticket """


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'review/create_ticket.html'
    form_class = TicketForm
    success_url = reverse_lazy('flux')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

# TODO
#  1: Déplacer les class form dans un fichier forms.py
#  2: Nettoyer les vues & templates inutilisé
#  3: Permettre a un utilisateur de se désabonner d'un utilisateur suivis
#  4: Mettre en place la page post qui contiendra les critiques lié au ticket créer

