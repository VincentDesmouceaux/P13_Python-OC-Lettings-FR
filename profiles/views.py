# profiles/views.py
from django.shortcuts import render, get_object_or_404
from .models import Profile


def index(request):
    profiles_list = Profile.objects.select_related("user").all()
    return render(request, "profiles/index.html", {"profiles_list": profiles_list})


def detail(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, "profiles/profile.html", {"profile": profile})
