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

    def __str__(self):
        return f"Critique de {self.ticket.title} par {self.user.username}, Note: {self.rating}"

    def get_star_rating(self):
        # Créer une chaîne d'étoiles en fonction de la note attribuée
        return '★' * self.rating

    def get_absolute_url(self):
        return reverse('update_review', args=[str(self.pk)])


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

