# lettings/views.py
from django.shortcuts import render, get_object_or_404
from .models import Letting


def index(request):
    """Liste de toutes les locations."""
    lettings_list = Letting.objects.select_related("address").all()
    return render(request, "lettings/index.html", {"lettings_list": lettings_list})


def detail(request, letting_id):
    """Page d’un seul letting."""
    letting = get_object_or_404(Letting, id=letting_id)
    context = {"title": letting.title, "address": letting.address}
    return render(request, "lettings/letting.html", context)
