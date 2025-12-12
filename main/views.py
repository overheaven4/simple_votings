from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login


def my_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return login("auth")
        ...
    else:
        # Return an 'invalid login' error message.
        ...