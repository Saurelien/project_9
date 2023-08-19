from django import forms
from .models import Ticket, Review, Article
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
        fields = ['title', 'description', 'rating', 'parent_review']
        widgets = {
            'rating': forms.HiddenInput(),
            'parent_review': forms.HiddenInput(),
        }


class ArticleCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

    review_title = forms.CharField(
        label='Titre de la critique',
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Titre de la critique'}),
    )
    review_description = forms.CharField(
        label='Description de la critique',
        widget=forms.Textarea(attrs={'placeholder': 'Description de la critique'}),
        required=True,
    )
