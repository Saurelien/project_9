from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Nom d'utilisateur *", error_messages={'required': "Veuillez remplir ce champ*"})
    password1 = forms.CharField(label="Mot de passe *", error_messages={'required': "Veuillez remplir ce champ*"})
    password2 = forms.CharField(label="Confirmez le mot de passe *",
                                error_messages={'required': "Veuillez remplir ce champ*"})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("La confirmation du mot de passe ne correspond pas à la saisie du mot de passe.")

        return cleaned_data

