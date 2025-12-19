import datetime

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
def index_page(request):
    context = {
       print("Войдите в аккаунт")
    }
    return render(request, "index.html", context)




def my_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return login("auth")

    else:
        # Return an 'invalid login' error message.
        return render(request,"login.html")
        print("Did you forget your username or password?Are you stupied?")
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/')
# Create your views here.