from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import RegistrationForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("Le formulaire est validé")
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(request, username=username, password=password)
            login(request, authenticated_user)
            return redirect('skeleton')
    else:
        form = RegistrationForm()
    return render(request, 'authenticator/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(User.objects.all())
            return redirect('flux')  # Redirige vers la page des tickets SI la connexion REUSSIT
        else:
            return render(request, 'skeleton.html', {'erreurs': 'Identifiants invalides'})
    return render(request, 'skeleton.html')


def get_all_info():
    users = User.objects.all()
    for user in users:
        print(f"Username: {user.username}")


def user_logout(request):
    logout(request)
    return redirect('login')
