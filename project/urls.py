"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# import les vues de l'app authenticator
# importe la vue du projet pour une page d'acceuille
from .views import skeleton_view
from authenticator.views import RegisterView, LoginView, ListAllUser
# from review.views import FluxView

app_name = 'authenticator'

urlpatterns = [
    path('', skeleton_view, name='skeleton'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', ListAllUser.as_view(), name='user_list'),
    # path('flux/', FluxView.as_view(), name='flux')
    path('admin/', admin.site.urls),
]
