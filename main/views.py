from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Voting, VotingOption, Vote
from django import forms
from main.forms.forms import VotingForm
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def voting(request, voting_id):
    voting = get_object_or_404(Voting, id=voting_id)
    context = {
        "voting": voting,
    }
    options_list = VotingOption.objects.filter(voting=voting)
    is_voted = False
    for option in options_list:
        vote_list = Vote.objects.filter(option=option)
        for vote in vote_list:
            if vote.user == request.user:
                is_voted = True
                context['given_vote'] = vote.option
                break
        if is_voted: break
    if is_voted:
        template_name = "voting_result.html"
        options = []
        for i in range(len(options_list)):
            votes_count = Vote.objects.filter(option=options_list[i]).count()
            options.append((options_list[i], votes_count))
        context['options_list'] = options

    else:
        template_name = "voting.html"
        if request.method == "POST":
            form = VotingForm(request.POST, voting=voting)
            if form.is_valid():
                option = form.cleaned_data['option']
                Vote.objects.create(user=request.user, option=option)
                return redirect(f'/voting/{voting_id}')

        else:
            form = VotingForm(voting=voting)
        context['form'] = form
    return render(request, template_name, context)
#
# def index_page(request):
#     context = {
#        print("Войдите в аккаунт")
#     }
#     return render(request, "login_register.html", context)


def index_view(request):
    pass






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

def logout_view(request):
    logout(request)
    return redirect('/')

def registration_page(request):
    return render(request,"reg.html", {})

def profile(request, username):
    if request.method == "POST":
        return redirect(f'/profile/{username}/edit')
    else:
        user = get_object_or_404(User, username=username)
        context = {
            'user':user,
        }
        vote_list = Vote.objects.filter(user=user)
        option_list = []
        for vote in vote_list:
            option_list.append(vote.option)
        context['options'] = option_list

        return render(request, "profile.html", context)
def profile_edit(request, username):
    if request.user.username == username or request.user.is_superuser:
        context = {}
        return render(request, "profile_edit.html", context)
    else:
        return render(request, "error.html", {'error_text':'access is denied'})

@login_required
def new_vote_page(request):
    if request.method == "POST":
        # Получаем данные из формы
        title = request.POST.get('title')
        question = request.POST.get('question')  # в моделях это description
        options = request.POST.getlist('option')

        # Проверяем обязательные поля
        if not title or not question:
            messages.error(request, 'Заполните все обязательные поля')
            return redirect('new_vote')  # перенаправляем обратно с сообщением

        # Создаем голосование
        new_voting = Voting.objects.create(
            title=title,
            description=question,
            creator=request.user
        )

        # Создаем варианты ответов
        for option_text in options:
            if option_text.strip():  # проверяем, что вариант не пустой
                VotingOption.objects.create(
                    voting=new_voting,
                    text=option_text
                )

        messages.success(request, 'Голосование создано успешно!')
        return redirect(f'/voting/{new_voting.id}')

    return render(request, "create.html", {})

def votes_page(request):
    context = {
        "items": Voting.objects.all()

    }
    return render(request,"votes.html",context)