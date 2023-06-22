from django.shortcuts import render


def skeleton_view(request):
    return render(request, 'skeleton.html')
