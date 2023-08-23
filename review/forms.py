from django import forms
from .models import Ticket, Review
from django.core.validators import MinValueValidator, MaxValueValidator


class FollowUserForm(forms.Form):
    username = forms.CharField()


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'description', 'rating']


class TicketAndReviewForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

    rating = forms.IntegerField(
        label="Note",
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    critique_title = forms.CharField(label="Titre de la critique")
    critique_description = forms.CharField(
        label="Description de la critique",
        widget=forms.Textarea
    )
