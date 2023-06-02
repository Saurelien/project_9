from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=200)
    descritpion = models.TextField(max_length=2048)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on delete=)