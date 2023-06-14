from .models import *
from django.db.models import Q
from random import choice
from django.conf import settings


def random_color(request):
    colors = [
        "success",
        "danger",
        "warning",
        "black",
        "primary",
        "link",
        "info",
        "dark",
        "white",
        "light",
    ]
    return {"random_color": choice(colors)}


def user_transactions(request):
    if request.user.is_authenticated:
        return {
            "user_transactions": Transaction.objects.filter(
                Q(sender=request.user.account) | Q(receiver=request.user.account)
            )
        }
    else:
        return {}


def webhost(request):
    return {"WEBHOST": settings.WEBHOST}
