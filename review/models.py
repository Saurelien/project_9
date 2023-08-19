from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='ticket_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('update_ticket', args=[str(self.pk)])

    def ticket_critiques(self):
        """
        Je défini une relation ForeignKey entre le modèle Review et le modèle Ticket,
        ce qui signifie qu'un Ticket peut avoir plusieurs critiques associées,
        et chaque Review est liée à un seul Ticket.
        """
        return self.review_set.all()

    def __str__(self):
        return self.title


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0
    )
    title = models.CharField(max_length=200, default="")
    description = models.TextField(default="")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_order = models.PositiveIntegerField(default=0)
    parent_review = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Critique de {self.ticket.title} par {self.user.username}, Note: {self.rating}"

    def get_star_rating(self):
        # Créer une chaîne d'étoiles en fonction de la note attribuée
        return '★' * self.rating

    def get_absolute_url(self):
        return reverse('update_review', args=[str(self.pk)])

    def ticket_critiques(self):
        return Review.objects.filter(ticket=self).select_related('user', 'parent_review')


class UserFollows(models.Model):
    # Utilisateurs suivis
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    # Utilisateur abonnés
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'followed_user')

    def __str__(self):
        return f'{self.follower} follows {self.followed_user}'


class ActionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100)
    action_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action_type}"


class Article(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, default="")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, default="")
    created_at = models.DateTimeField(auto_now_add=True)


"""
Le modèle Ticket et le modèle Review définissent une relation de clé étrangère entre eux.
Chaque ticket peut avoir plusieurs critiques, et chaque critique est liée à un seul ticket.

La méthode ticket_critiques(self) dans le modèle Ticket permet de récupérer
toutes les critiques associées à ce ticket spécifique en utilisant la relation ForeignKey inversée.

La vue FluxView est utilisée pour afficher le flux d'un utilisateur connecté.
Elle récupère les utilisateurs suivis par l'utilisateur connecté, puis utilise la fonction get_posts(users)
pour obtenir les publications des utilisateurs suivis. Elle filtre et organise ensuite les publications
pour les afficher dans le flux de l'utilisateur.

Dans FluxView, pour chaque publication (ticket ou critique),
la vue vérifie si c'est un ticket en fonction de la valeur de post.content_type. Si c'est un ticket,
elle vérifie si l'ID du ticket a déjà été ajouté à l'ensemble tickets_added pour éviter les doublons.
Si l'ID n'est pas dans tickets_added,
elle ajoute les critiques associées à ce ticket à l'aide de post.ticket.ticket_critiques()
(utilisant la méthode définie dans le modèle Ticket).

La vue PostsView affiche les tickets créés par l'utilisateur connecté et
les tickets associés aux critiques des utilisateurs qu'il suit. Cela permet à
l'utilisateur de voir les tickets auxquels il a contribué ainsi que les tickets associés aux critiques
de ses utilisateurs suivis.

En résumé, les interactions dans le code concernent la récupération,
la filtration et l'affichage des publications (tickets et critiques)
dans le flux de l'utilisateur connecté (FluxView) et l'affichage des tickets dans la vue PostsView.
"""
