from django import template

register = template.Library()


@register.filter
def has_reviewed(ticket, user):
    """Filtre qui vérifie si l'utilisateur a déjà écrit une critique pour un ticket"""
    return ticket.reviews.filter(user=user).exists()


@register.filter
def sort_reviews_by_date(ticket):
    """Filtre qui trie les critiques d'un ticket par ordre antéchronologique"""
    return ticket.reviews.all().order_by('-created_at')
