from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FollowUserForm, TicketForm, TicketUpdateForm, ReviewForm
from django.views.generic.edit import FormView, UpdateView, CreateView
from review.models import UserFollows, Review, Ticket
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms
from django.views.generic import DeleteView
from itertools import chain
from django.db.models import CharField, Value
from django.db.models import Q


UserModel = get_user_model()


def get_posts(users):
    reviews = Review.objects.filter(user__in=users)
    reviews = reviews.annotate(content_type=Value('CRITIQUE', CharField()))

    # Utilisation de Q pour combiner des conditions de filtrage
    tickets = Ticket.objects.filter(Q(creator__in=users) | Q(review__user__in=users))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # Obtenir toutes les critiques associées aux tickets des utilisateurs suivis
    ticket_ids = tickets.values_list('id', flat=True)
    associated_reviews = Review.objects.filter(ticket_id__in=ticket_ids)
    associated_reviews = associated_reviews.annotate(content_type=Value('CRITIQUE', CharField()))

    # Combiner et trier les trois types de posts
    return sorted(
        chain(reviews, tickets, associated_reviews),
        key=lambda post: post.created_at,
        reverse=True
    )


class FluxView(LoginRequiredMixin, TemplateView):
    template_name = 'review/flux.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer les utilisateurs suivis par l'utilisateur connecté
        utilisateurs_suivis = self.request.user.following.all()

        # Créez une liste d'utilisateurs à partir des utilisateurs suivis
        users = [user.followed_user for user in utilisateurs_suivis]

        # Utiliser la fonction get_posts pour obtenir les posts des utilisateurs suivis
        context['posts'] = get_posts(users)

        return context


class PostsView(LoginRequiredMixin, TemplateView):
    template_name = 'review/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = get_posts([self.request.user])
        return context


class SubscribeUserView(View):
    """
Définir une méthode comme statique (@staticmethod) dans une vue basée sur classe en Django n'est pas obligatoire et,
 en fait, c'est généralement déconseillé pour les méthodes de traitement de requêtes HTTP comme post ou get.
    """
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


""" Classe prototype pour le systeme d'abonnement utilisateur"""


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


class TicketDeleteView(DeleteView):
    model = Ticket
    # Redirige vers la page flux après la suppression du ticket
    success_url = reverse_lazy('posts')
    # Créez ce template pour demander confirmation à l'utilisateur avant de supprimer le ticket
    template_name = 'review/delete_ticket.html'

    def delete(self, request, *args, **kwargs):
        ticket = self.get_object()
        print(f"Le ticket '{ticket.title}' a été supprimé le {ticket.created_at} par {request.user}")
        messages.success(request, f"Le ticket '{ticket.title}' a été supprimé avec succès.")
        return super().delete(request, *args, **kwargs)


""" Vues creation et mise à jour des critiques """


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/create_review.html'
    success_url = reverse_lazy('flux')  # Mettez l'URL de redirection souhaitée après la création de la critique

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get('ticket_id')
        ticket = get_object_or_404(Ticket, id=ticket_id)
        context['ticket'] = ticket
        return context

    def form_valid(self, form):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = Ticket.objects.filter(id=ticket_id).first()

        if ticket:
            form.instance.ticket = ticket
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            messages.error(self.request, "Le ticket spécifié n'existe pas.")
            return redirect('flux')


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    template_name = 'review/update_review.html'
    form_class = ReviewForm
    success_url = '/flux/'


# TODO
#  2: Nettoyer les vues & templates inutilisé
#  3: Permettre a un utilisateur de se désabonner d'un utilisateur suivis
#  4: Mettre en place la page post qui contiendra les critiques lié au ticket créer

