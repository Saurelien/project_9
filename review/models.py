from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """
    Class servant a tracer les erreur remonté par les utlisateurs
    """
    STATUS_CHOICES = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    assigned_to = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # Add any other fields you need, such as priority, due date, etc.

    def __str__(self):
        return self.title


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    # Your UserFollows model definition goes here

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )
