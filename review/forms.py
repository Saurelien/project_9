from django import forms
from .models import Ticket
from .models import PrivateMessage


class FollowUserForm(forms.Form):
    username = forms.CharField()


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image', 'note']


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image', 'note']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
        }


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['recipient', 'subject', 'message']