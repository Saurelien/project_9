from django.contrib.auth.forms import UserCreationForm, User, AuthenticationForm
from django.contrib.auth import login
from django.views.generic import FormView, ListView
from django.contrib.auth.views import LogoutView


class RegisterView(FormView):
    template_name = 'authenticator/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)


class LoginView(FormView):
    template_name = 'authenticator/login.html'
    form_class = AuthenticationForm
    success_url = '/flux/'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutUserView(LogoutView):
    next_page = 'login'


class ListAllUser(ListView):
    model = User
    template_name = 'authenticator/user_list.html'
    context_object_name = 'users'
