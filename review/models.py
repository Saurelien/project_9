from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse


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
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0
    )
    # Headline
    title = models.CharField(max_length=128, default="")
    # Body
    description = models.TextField(max_length=8192, blank=True, default="")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Critique de {self.ticket.title} par {self.user.username}, Note: {self.rating}"

    def get_star_rating(self):
        # Créer une chaîne d'étoiles en fonction de la note attribuée
        return '★' * self.rating

    def get_absolute_url(self):
        return reverse('update_review', args=[str(self.pk)])


class UserFollows(models.Model):
    # Utilisateurs suivis " User "
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    # Utilisateur abonnés " followed_user
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'followed_user')

    def __str__(self):
        return f'{self.follower} follows {self.followed_user}'

