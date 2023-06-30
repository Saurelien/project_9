from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


def skeleton_view(request):
    return render(request, 'skeleton.html', {'user': request.user})


class SkeletonUserOnlineView(LoginRequiredMixin, TemplateView):
    template_name = 'skeleton_user_online.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('authenticator:skeleton')
        return super().dispatch(request, *args, **kwargs)
