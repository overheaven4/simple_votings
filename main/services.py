from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import Voting, VotingOption, Vote
from django.contrib.auth.models import User


def get_popular_votings(limit=5):
    """
    Возвращает список самых популярных голосований
    на основе количества отданных голосов.
    """
    # Аннотируем голосования количеством связанных объектов Vote
    votings = Voting.objects.annotate(
        total_votes=Count('votingoption__vote')
    ).order_by('-total_votes')[:limit]

    return votings


def get_user_voting_statistics(user: User) -> dict:
    """
    Собирает подробную статистику активности пользователя
    для отображения в его профиле.
    """
    if not user.is_authenticated:
        return {}

    total_votes_cast = Vote.objects.filter(user=user).count()
    created_votings_count = Voting.objects.filter(creator=user).count()

    # Ищем, в скольких уникальных опросах участвовал юзер
    unique_votings_participated = Vote.objects.filter(
        user=user
    ).values('option__voting').distinct().count()

    return {
        'username': user.username,
        'total_votes': total_votes_cast,
        'created_votings': created_votings_count,
        'unique_participations': unique_votings_participated,
        'is_active_voter': total_votes_cast > 10
    }


def check_user_can_vote(user: User, voting_id: int) -> bool:
    """
    Проверяет, имеет ли право пользователь голосовать в данном опросе
    (не голосовал ли он ранее).
    """
    voting = get_object_or_404(Voting, id=voting_id)
    has_voted = Vote.objects.filter(
        user=user,
        option__voting=voting
    ).exists()

    return not has_voted