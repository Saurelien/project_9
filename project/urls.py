"""
URL configuration for project.

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
from authenticator.views import RegisterView, LogoutUserView, LoginView
from review.views import (
    FluxView, FollowUserView, TicketCreateView, PostsView,
    UnfollowUserView, SubscribeUserView, TicketUpdateView, TicketDeleteView,
    CreateReviewView, UpdateReviewView, DeleteReviewView, CreateTicketAndReviewView)
from django.conf import settings
from django.conf.urls.static import static


app_name = 'authenticator'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('flux/', FluxView.as_view(), name='flux'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('subscribe/', SubscribeUserView.as_view(), name='subscribe_user'),
    path('abonnements/', FollowUserView.as_view(), name='flux_utilisateurs'),
    path('create_ticket/', TicketCreateView.as_view(), name='create_ticket'),
    path('posts/', PostsView.as_view(), name='posts'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('ticket/<int:pk>/update/', TicketUpdateView.as_view(), name='update_ticket'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='delete_ticket'),
    path('review/<int:pk>/delete/', DeleteReviewView.as_view(), name='delete_review'),
    path('create_review/<int:ticket_id>/', CreateReviewView.as_view(), name='create_review'),
    path('review/<int:pk>/update', UpdateReviewView.as_view(), name='update_review'),
    path('review/', CreateTicketAndReviewView.as_view(), name='review'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
