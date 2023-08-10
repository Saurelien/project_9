from django import forms
from django.contrib.auth import get_user_model
from .models import PrivateMessage


UserModel = get_user_model()


class PrivateMessageForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = PrivateMessage
        fields = ['recipients', 'subject', 'message']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Récupérer la liste des utilisateurs suivis pour le champ "recipients"
        self.fields['recipients'].queryset = user.following.all()
