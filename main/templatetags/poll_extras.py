from django import template
from main.models import Vote, VotingOption

register = template.Library()


@register.filter(name='percentage')
def percentage(value, arg):
    """
    Вычисляет процент от числа.
    Использование в шаблоне: {{ votes_count|percentage:total_votes }}
    """
    try:
        value = int(value)
        arg = int(arg)
        if arg == 0:
            return "0%"
        result = (value / arg) * 100
        return f"{result:.1f}%"
    except (ValueError, ZeroDivisionError, TypeError):
        return "0%"


@register.simple_tag
def get_total_votes_for_voting(voting):
    """
    Возвращает общее количество голосов для переданного объекта Voting.
    Использование: {% get_total_votes_for_voting voting_obj as total %}
    """
    if not voting:
        return 0

    options = VotingOption.objects.filter(voting=voting)
    total_votes = 0

    for option in options:
        total_votes += Vote.objects.filter(option=option).count()

    return total_votes


@register.filter(name='has_voted')
def has_voted(voting, user):
    """
    Проверяет, голосовал ли пользователь в конкретном опросе.
    Использование: {% if voting|has_voted:request.user %}
    """
    if not user.is_authenticated:
        return False
    return Vote.objects.filter(user=user, option__voting=voting).exists()