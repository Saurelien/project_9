from django import forms
from django.contrib.auth.forms import UserCreationForm, User, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.generic import FormView, ListView


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Nom d'utilisateur *", error_messages={'required': "Veuillez remplir ce champ*"})
    password1 = forms.CharField(label="Mot de passe *", error_messages={'required': "Veuillez remplir ce champ*"})
    password2 = forms.CharField(label="Confirmez le mot de passe *",
                                error_messages={'required': "Veuillez remplir ce champ*"})

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("La confirmation du mot de passe ne correspond pas à la saisie du mot de passe")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé !")

        return cleaned_data


class RegisterView(FormView):
    template_name = 'authenticator/register.html'
    form_class = RegistrationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        authenticated_user = authenticate(request=self.request, username=username, password=password)
        login(self.request, authenticated_user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'authenticator/login.html'
    form_class = AuthenticationForm
    success_url = '/'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class ListAllUser(ListView):
    model = User
    template_name = 'authenticator/user_list.html'
    context_object_name = 'users'
