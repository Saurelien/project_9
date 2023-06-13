from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from authenticator.models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"Nouvel utilisateur enregistré : {user.username} ({user.email})")
            # Envoyer l'email de notification
            user.send_registration_email()
            login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'authenticator/register.html', {'form': form})


def get_registered_users():
    users = User.objects.all()
    for user in users:
        print(user.email)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige vers la page d'accueil "SI"" la connexion "REUSSIT"
    return render(request, 'authenticator/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def reset_password(request):
    user_password = request.GET['password']
    new_password = request.POST[user_password]
    return new_password
