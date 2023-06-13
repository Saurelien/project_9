from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Adresse e-mail", error_messages={'required': "Veuillez remplir ce champ*"})
    first_name = forms.CharField(label="Prénom", error_messages={'required': "Veuillez remplir ce champ*"})
    last_name = forms.CharField(label="Nom de famille", error_messages={'required': "Veuillez remplir ce champ*"})
    password1 = forms.CharField(label="Mot de passe", error_messages={'required': "Veuillez remplir ce champ*"})
    password2 = forms.CharField(label="Confirmez le mot de passe",
                                error_messages={'required': "Veuillez remplir ce champ*"})
