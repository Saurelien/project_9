from django import forms
from django.forms import ClearableFileInput

from .models import Ticket, Review


class FollowUserForm(forms.Form):
    username = forms.CharField()


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'widgets/custom_clearable_file_input.html'


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'image': CustomClearableFileInput()
        }


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(6)],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Review
        fields = ['title', 'description', 'rating']


class TicketAndReviewForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
    rating = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(6)],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )
    critique_title = forms.CharField(label="Titre de la critique")
    critique_description = forms.CharField(
        label="Commentaire",
        widget=forms.Textarea
    )
