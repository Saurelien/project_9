from django.contrib.auth.forms import UserCreationForm, User, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import FormView, ListView, RedirectView
from django.contrib.auth.views import LogoutView


"""
Compréhension de la méthode generique de UserCreationForm & AuthenticationForm:

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

        # Vérifie la concordance des mots de passe
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("La confirmation du mot de passe ne correspond pas à la saisie du mot de passe")
        # Vérifier si le nom d'utilisateur est déjà utilisé
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé !")

        return cleaned_data
        
class LoginView(DjangoLoginView):
    template_name = 'authenticator/login.html'
    form_class = AuthenticationForm
    success_url = '/flux/'

    def post_user(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            # Verifier si l'utilisateur est inscrit
            if user is not None:
                login(request, user)
                return redirect(self.success_url)
            else:
                messages.error(request, "Vous devez être inscrit pour vous connecter.")

        return self.form_invalid(form)
        
"""


class RegisterView(FormView):
    template_name = 'authenticator/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)


class LoginView(FormView):
    template_name = 'authenticator/flux.html'
    form_class = AuthenticationForm
    success_url = '/flux/'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutUserView(LogoutView):
    next_page = 'skeleton'

    # def get(self, request, *args, **kwargs):
    #     logout(request)
    #     return super().get(request, *args, **kwargs)


class ListAllUser(ListView):
    model = User
    template_name = 'authenticator/user_list.html'
    context_object_name = 'users'

# TODO Faire en sorte que le template skeleton_user_online affiche uniquement la page d'accueil pour un utilisateur
#  authentifié, un block contenant :
#     {% if user.is_authenticated %}
#         <div class="block">
#             <h2 class="block-title">Bienvenue, {{ user.username }}</h2>
#             <a href="{% url 'flux' %}" class="flux-link">Accéder au flux</a>
#             <a href="{% url 'authenticator:logout' %}" class="logout-button">Se déconnecter</a>
#             <a href="{% url 'authenticator:user_list' %}" class="btn btn-primary">Afficher la liste des utilisateurs</a>
#         </div>
#     {% else %}

