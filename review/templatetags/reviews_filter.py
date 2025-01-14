from django import template

register = template.Library()


@register.filter
def has_reviewed(ticket, user):
    """Vérifie si l'utilisateur a déjà écrit une critique pour un ticket donné."""
    return ticket.reviews.filter(user=user).exists()


@register.filter
def sort_reviews_by_date(ticket):
    """Trie les critiques d'un ticket par date de création, antéchronologique."""
    return ticket.reviews.all().order_by('-created_at')
