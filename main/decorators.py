from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from functools import wraps
from .models import Voting
from django.http import HttpResponseBadRequest


def user_is_voting_creator(function):
    """
    Декоратор проверяет, является ли текущий пользователь
    создателем голосования. Полезно для функций редактирования/удаления.
    """

    @wraps(function)
    def wrap(request, *args, **kwargs):
        voting_id = kwargs.get('voting_id')
        if not voting_id:
            raise ValueError("Декоратор требует передачи voting_id в URL")

        voting = get_object_or_404(Voting, id=voting_id)

        # Разрешаем доступ автору или суперпользователю (админу)
        if voting.creator == request.user or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied("У вас нет прав для изменения этого голосования.")

    return wrap


def ajax_required(function):
    """
    Декоратор для проверки, что запрос пришел через AJAX.
    Блокирует прямые переходы по ссылкам API.
    """

    @wraps(function)
    def wrap(request, *args, **kwargs):
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        is_fetch = request.headers.get('sec-fetch-mode') == 'cors'

        if not (is_ajax or is_fetch):
            return HttpResponseBadRequest(
                "Этот эндпоинт доступен только для AJAX/Fetch запросов"
            )

        return function(request, *args, **kwargs)

    return wrap