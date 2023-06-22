from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def skeleton_view(request):
    # Vérifier si la base de données contient des utilisateurs enregistrés
    if User.objects.count() == 0:
        return render(request, 'skeleton.html')
    else:
        # Rediriger vers une autre page si la base de données n'est pas vide
        return redirect('skeleton')  # Remplacez 'register' par l'URL souhaitée

