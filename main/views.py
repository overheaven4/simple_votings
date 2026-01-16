from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Voting, VotingOption


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
        return render(request, "create.html", {})

    return render(request, "create.html", {})
