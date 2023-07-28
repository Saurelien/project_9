from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FollowUserForm, TicketForm, TicketUpdateForm
from django.views.generic.edit import FormView, UpdateView
from review.models import UserFollows
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView  # ListView
from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Ticket
from django.contrib import messages
from django import forms

UserModel = get_user_model()


class FluxView(LoginRequiredMixin, TemplateView):
    template_name = 'review/flux.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer les utilisateurs suivis par l'utilisateur connecté
        utilisateurs_suivis = self.request.user.following.all()

        # Ajouter les utilisateurs suivis au contexte
        context['utilisateurs_suivis'] = utilisateurs_suivis

        return context


class PostsView(LoginRequiredMixin, TemplateView):
    template_name = 'review/posts.html'


class SubscribeUserView(View):
    def post(self, request):
        username = request.POST.get('username')
        if username:
            # Recherche de l'utilisateur à suivre
            user_to_follow = UserModel.objects.filter(username=username).first()

            # S'assurer que l'utilisateur existe avant de le suivre
            if user_to_follow:
                # Vérifier si la relation de suivi existe déjà
                if not UserFollows.objects.filter(follower=request.user, followed_user=user_to_follow).exists():
                    # Créer la relation de suivi
                    UserFollows.objects.create(follower=request.user, followed_user=user_to_follow)
                    messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")
                else:
                    messages.error(request, f"Vous suivez déjà {user_to_follow.username}.")

        return redirect('flux_utilisateurs')


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


class UnfollowUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')
        followed_user = get_object_or_404(UserModel, username=username)

        # Vérifiez si la relation de suivi existe avant de la supprimer
        try:
            follow_relation = UserFollows.objects.get(follower=request.user, followed_user=followed_user)
            follow_relation.delete()
        except UserFollows.DoesNotExist:
            pass

        # Rediriger l'utilisateur vers une page appropriée (par exemple, la liste des utilisateurs suivis)
        return redirect('flux_utilisateurs')


""" Vue de la gestion des tickets """
""" Consommation du model Ticket """


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'review/create_ticket.html'
    form_class = TicketForm
    success_url = reverse_lazy('posts')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            # Si un ticket_id est fourni dans l'URL, récupérez le ticket existant
            ticket = get_object_or_404(Ticket, id=ticket_id)
            # Pré-remplissez les champs du formulaire avec les valeurs du ticket existant
            form.initial['title'] = ticket.title
            form.initial['description'] = ticket.description
            form.initial['image'] = ticket.image
            # Masquer le champ "note" dans le formulaire car il sera géré séparément
            form.fields['note'].widget = forms.HiddenInput()
        return form

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


""" Mettre à jour ou supprimer le ticket """


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    template_name = 'review/update_ticket.html'
    form_class = TicketUpdateForm
    success_url = '/posts/'


# TODO
#  2: Nettoyer les vues & templates inutilisé
#  3: Permettre a un utilisateur de se désabonner d'un utilisateur suivis
#  4: Mettre en place la page post qui contiendra les critiques lié au ticket créer

