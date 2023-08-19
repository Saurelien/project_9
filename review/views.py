from django.contrib.auth.mixins import LoginRequiredMixin
from review.forms import FollowUserForm, TicketForm, TicketUpdateForm, ReviewForm, ArticleCreationForm
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
from django.db.models import Q, CharField, Value
from django.db.models.functions import Concat
from PIL import Image
import uuid
from django.conf import settings
from pathlib import Path
from itertools import chain


UserModel = get_user_model()


def get_posts(users):
    reviews = Review.objects.filter(user__in=users).annotate(content_type=Value('CRITIQUE', CharField()))

    tickets = Ticket.objects.filter(Q(creator__in=users) | Q(review__user__in=users)).annotate(
        content_type=Value('TICKET', CharField()),
        ticket_title=Concat('title', Value(' (Ticket)'), output_field=CharField())
    )

    return sorted(
        chain(reviews, tickets),
        key=lambda post: post.created_at,
        reverse=True
    )


class FluxView(LoginRequiredMixin, TemplateView):
    """
    Vue pour afficher le flux de l'utilisateur avec des publications filtrées et organisées.
    Cette vue récupère les publications (à la fois les tickets et les critiques)
    des utilisateurs suivis par l'utilisateur connecté,
    les organise pour éliminer les doublons de tickets, et les affiche dans un format convivial.
    """
    template_name = 'review/flux.html'

    def get_context_data(self, **kwargs):
        """
        Récupère et organise les publications pour les afficher dans le flux de l'utilisateur.
        Retourne un dictionnaire contenant les critiques organisées et filtrées.
        """
        context = super().get_context_data(**kwargs)

        # Récupérer les utilisateurs suivis par l'utilisateur connecté
        utilisateurs_suivis = self.request.user.following.all()

        # Créer une liste d'utilisateurs à partir des utilisateurs suivis
        users = [user.followed_user for user in utilisateurs_suivis]

        # Utiliser la fonction get_posts pour obtenir les posts des utilisateurs suivis
        posts = get_posts(users)

        # Créer un ensemble pour suivre les IDs des tickets déjà ajoutés
        tickets_added = set()

        # Filtrer les doublons et trier les critiques par date de création
        filtered_posts = []
        for post in posts:
            if post.content_type == 'TICKET':
                if post.pk not in tickets_added:
                    tickets_added.add(post.pk)
                    post.ticket_critiques = sorted(post.ticket_critiques(),
                                                   key=lambda x: x.created_at,
                                                   reverse=True
                                                   )
                    filtered_posts.append(post)  # Ajouter le ticket filtré
            else:
                filtered_posts.append(post)  # Ajouter les critiques normales

        context['posts'] = filtered_posts

        return context


class PostsView(LoginRequiredMixin, TemplateView):
    template_name = 'review/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer les tickets créés par l'utilisateur
        user_tickets = Ticket.objects.filter(creator=self.request.user)

        # Récupérer les tickets associés aux critiques des utilisateurs suivis
        followed_users = UserFollows.objects.filter(follower=self.request.user).values('followed_user')
        followed_tickets = Ticket.objects.filter(creator__in=followed_users)

        context['user_tickets'] = user_tickets
        context['followed_tickets'] = followed_tickets

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
    success_url = reverse_lazy('flux')

    def form_valid(self, form):
        form.instance.creator = self.request.user

        image = form.cleaned_data['image']
        if image:
            image_name = f'ticket_{uuid.uuid4().hex}.jpg'  # Générer un nom de fichier unique
            img = Image.open(image)
            img.thumbnail((300, 300))
            img.save(Path(settings.MEDIA_ROOT) / 'ticket_images' / image_name)

            form.instance.image = f'ticket_images/{image_name}'  # Enregistrer le chemin de l'image

        return super().form_valid(form)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            context['ticket'] = ticket
            context['reviews'] = Review.objects.filter(ticket=ticket)
        return context


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    template_name = 'review/update_ticket.html'
    form_class = TicketUpdateForm
    success_url = '/posts/'


class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('posts')
    template_name = 'review/delete_ticket.html'

    def delete(self, request, *args, **kwargs):
        ticket = self.get_object()

        # Supprimer l'image du ticket s'il existe
        if ticket.image:
            try:
                # Supprimer le fichier d'image en utilisant PIL
                ticket.image.delete()
            except Exception as e:
                # Gérer les erreurs éventuelles spécifiques à Pillow
                messages.error(self.request, f"Erreur lors de la suppression de l'image : {e}")

        # Supprimer toutes les critiques liées à ce ticket
        ticket.critique_set.all().delete()
        messages.success(self.request, "Le ticket a été supprimé avec succès.")
        return super().delete(request, *args, **kwargs)


""" Vues creation et mise à jour des critiques """


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/create_review.html'

    def form_valid(self, form):
        ticket_id = self.kwargs['ticket_id']
        ticket = get_object_or_404(Ticket, pk=ticket_id)

        parent_review_id = self.request.POST.get('parent_review')
        parent_review = None
        if parent_review_id:
            parent_review = get_object_or_404(Review, pk=parent_review_id)

        form.instance.ticket = ticket
        form.instance.user = self.request.user
        form.instance.parent_review = parent_review

        form.save()

        # Redirect back to the ticket's detail page
        return redirect('flux')


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    template_name = 'review/update_review.html'
    form_class = ReviewForm
    success_url = '/flux/'


class DeleteReviewView(DeleteView):
    model = Review
    template_name = 'review/delete_review.html'
    context_object_name = 'critique'

    def get_success_url(self):
        # Rediriger l'utilisateur vers le flux ou une autre page après la suppression de la critique
        return reverse_lazy('flux')

    def delete(self, request, *args, **kwargs):
        critique = self.get_object()

        # Supprimer la critique
        critique.delete()

        messages.success(self.request, "La critique a été supprimée avec succès.")
        return super().delete(request, *args, **kwargs)


class CreateArticleView(FormView):
    template_name = 'review/article.html'
    form_class = ArticleCreationForm
    success_url = '/flux/'

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.creator = self.request.user
        ticket.save()

        image = form.cleaned_data['image']  # Obtenez l'image du formulaire

        if image:
            image_name = f'ticket_{uuid.uuid4().hex}.jpg'
            img = Image.open(image)
            img.thumbnail((300, 300))
            img.save(Path(settings.MEDIA_ROOT) / 'ticket_images' / image_name)

            ticket.image = f'ticket_images/{image_name}'
            ticket.save()

        # Créez une critique associée au ticket
        Review.objects.create(
            ticket=ticket,
            rating=form.cleaned_data['rating'],
            title=form.cleaned_data['review_title'],
            description=form.cleaned_data['review_description'],
            user=self.request.user
        )

        return super().form_valid(form)
