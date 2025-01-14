from django.conf import settings


def display_helper(request):
    return {
        "DISPLAY_HELPER": settings.DISPLAY_HELPER,
    }
