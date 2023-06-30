from django.contrib.auth.mixins import LoginRequiredMixin
from review.models import UserFollows
from django.shortcuts import get_object_or_404, reverse
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView  # ListView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic.base import View


class AbonnementView(TemplateView):
    template_name = 'review/abonnements.html'


class SearchUserView(View):
    def get(self, request):
        query = request.GET.get('q')
        if query and len(query) >= 3:
            users = User.objects.filter(username__startswith=query)
        else:
            users = []

        context = {'users': users}
        return render(request, 'review/recherche_utilisateur.html', context)


class FollowUserView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # Récupérer l'utilisateur à suivre ou une requete 404 not found si l'utilisateur n'existe pas " TEST "
        username = self.kwargs.get('username')
        followed_user = get_object_or_404(User, username=username)

        # Créer une relation de suivi entre l'utilisateur connecté et l'utilisateur suivi
        UserFollows.objects.get_or_create(follower=self.request.user, followed_user=followed_user)

        # Rediriger l'utilisateur vers une page appropriée (par exemple, le profil de l'utilisateur suivi)
        return reverse('user_profile', kwargs={'username': username})


class UnfollowUserView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # Récupérer l'utilisateur à ne plus suivre
        username = self.kwargs.get('username')
        followed_user = get_object_or_404(User, username=username)

        # Supprimer la relation de suivi entre l'utilisateur connecté et l'utilisateur suivi
        UserFollows.objects.filter(follower=self.request.user, followed_user=followed_user).delete()

        # Rediriger l'utilisateur vers une page appropriée (par exemple, le profil de l'utilisateur suivi)
        return reverse('user_profile', kwargs={'username': username})

# TODO Faire en sorte que le formulaire de recherche récupère les informations saisie par l'utilisateur
#  et affiche le nom de l'utilisateur saisie dans la recherche
#  pour le moment la recherche ne retourne pas d'erreurs mais aucuns utilisateurs selon la recherche n'est affiché ...
