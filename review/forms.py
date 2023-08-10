from django import forms
from .models import Ticket, Review


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
        widgets = {
            'rating': forms.HiddenInput(),
        }
