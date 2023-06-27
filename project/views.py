from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login


def skeleton_view(request):
    return render(request, 'skeleton.html', {'user': request.user})
