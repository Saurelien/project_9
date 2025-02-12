import os
from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

from review.forms import FollowUserForm, TicketForm, TicketUpdateForm, ReviewForm, TicketAndReviewForm
from django.views.generic import FormView, UpdateView, CreateView, ListView, TemplateView
from review.models import UserFollows, Review, Ticket
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms
from django.views.generic import DeleteView
from django.db.models import Q, CharField, Value
from PIL import Image
import uuid
from django.conf import settings
from pathlib import Path

UserModel = get_user_model()


class FluxView(LoginRequiredMixin, ListView):
    template_name = 'review/flux.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user

        followed_users = user.following.all().values_list('followed_user', flat=True)

        tickets = Ticket.objects.filter(
            Q(creator=user) | Q(creator__in=followed_users)
        ).annotate(content_type=Value('TICKET', CharField()))

        reviews = Review.objects.filter(
            Q(user=user) | Q(user__in=followed_users) | Q(ticket__creator=user)
        ).annotate(content_type=Value('REVIEW', CharField()))

        posts = sorted(
            chain(tickets, reviews),
            key=lambda post: post.created_at,
            reverse=True
        )

        return posts


class PostsView(LoginRequiredMixin, TemplateView):
    template_name = 'review/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Récupérer uniquement les tickets créés par l'utilisateur
        user_tickets = Ticket.objects.filter(creator=user).annotate(content_type=Value('ticket', CharField()))

        # Récupérer uniquement les critiques créées par l'utilisateur
        user_reviews = Review.objects.filter(user=user).annotate(content_type=Value('review', CharField()))

        # Fusionner les deux ensembles et trier par date de création
        combined_posts = sorted(
            chain(user_tickets, user_reviews),
            key=lambda post: post.created_at,
            reverse=True
        )

        context['combined_posts'] = combined_posts
        return context


class SubscribeUserView(View):

    def post(self, request):
        username = request.POST.get('username')
        if username:
            # Recherche de l'utilisateur à suivre
            user_to_follow = UserModel.objects.filter(username=username).first()

            # Vérifier si l'utilisateur existe
            if user_to_follow:
                if user_to_follow.username == request.user.username:
                    messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
                elif not UserFollows.objects.filter(follower=request.user,
                                                    followed_user=user_to_follow).exists():
                    # Créer la relation de suivi
                    UserFollows.objects.create(follower=request.user, followed_user=user_to_follow)
                    messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")
                else:
                    messages.error(request, f"Vous suivez déjà {user_to_follow.username}.")
            else:
                messages.error(request, "Cet utilisateur n'existe pas.")
        else:
            messages.error(request, "Veuillez entrer un nom d'utilisateur.")

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


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'review/create_ticket.html'
    form_class = TicketForm
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.creator = self.request.user

        image = form.cleaned_data['image']
        if image:
            try:
                ticket_images_path = Path(settings.MEDIA_ROOT) / 'ticket_images'

                # Créer le dossier s'il n'existe pas
                os.makedirs(ticket_images_path, exist_ok=True)

                image_name = f'ticket_{uuid.uuid4().hex}.jpg'
                img = Image.open(image)

                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.thumbnail((300, 300))
                img.save(ticket_images_path / image_name)
                form.instance.image = f'ticket_images/{image_name}'

            except Exception as e:
                raise ValidationError(f"Erreur lors du traitement de l'image : {str(e)}")

        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            form.initial['title'] = ticket.title
            form.initial['description'] = ticket.description
            form.initial['image'] = ticket.image
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
    success_url = '/flux/'


class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('posts')
    template_name = 'review/delete_ticket.html'

    def delete(self, request, *args, **kwargs):
        ticket = self.get_object()

        if ticket.image:
            try:
                ticket.image.delete()
            except Exception as e:

                messages.error(self.request, f"Erreur lors de la suppression de l'image : {e}")

        ticket.critique_set.all().delete()
        messages.success(self.request, "Le ticket a été supprimé avec succès.")
        return super().delete(request, *args, **kwargs)


""" Vues creation et mise à jour des critiques """


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/create_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs['ticket_id']
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        context['ticket'] = ticket
        return context

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
        return reverse_lazy('posts')

    def delete(self, request, *args, **kwargs):
        critique = self.get_object()
        critique.delete()

        messages.success(self.request, "La critique a été supprimée avec succès.")
        return super().delete(request, *args, **kwargs)


class CreateTicketAndReviewView(LoginRequiredMixin, CreateView):
    template_name = 'review/review.html'
    form_class = TicketAndReviewForm
    success_url = reverse_lazy('flux')

    def form_valid(self, form):
        image = form.cleaned_data['image']
        if image:
            # Définir le chemin complet du dossier où les images seront stockées
            ticket_images_path = Path(settings.MEDIA_ROOT) / 'ticket_images'

            # Créer le dossier s'il n'existe pas
            os.makedirs(ticket_images_path, exist_ok=True)

            image_name = f'ticket_{uuid.uuid4().hex}.jpg'
            img = Image.open(image)
            img.thumbnail((300, 300))
            img.save(ticket_images_path / image_name)

            form.instance.image = f'ticket_images/{image_name}'

        ticket = form.save(commit=False)
        ticket.creator = self.request.user
        ticket.save()

        # Créez la critique associée
        critique = Review(
            ticket=ticket,
            rating=form.cleaned_data['rating'],
            title=form.cleaned_data['critique_title'],
            description=form.cleaned_data['critique_description'],
            user=self.request.user
        )
        critique.save()

        return super().form_valid(form)