from main.models import Voting, Vote
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


def global_stats(request):
    """
    Контекстный процессор, который добавляет глобальную статистику
    платформы во все HTML шаблоны.
    """
    # Оборачиваем в try-except на случай, если таблицы еще не созданы
    try:
        total_users = User.objects.count()
        total_votings = Voting.objects.count()
        total_votes = Vote.objects.count()

        # Получаем самое последнее голосование
        latest_voting = Voting.objects.order_by('-created_at').first()
        latest_voting_title = latest_voting.title if latest_voting else "Нет активных опросов"

        # Считаем количество голосований, созданных за последние 24 часа
        yesterday = timezone.now() - datetime.timedelta(days=1)
        new_votings_today = Voting.objects.filter(created_at__gte=yesterday).count()

        return {
            'GLOBAL_STATS': {
                'total_users': total_users,
                'total_votings': total_votings,
                'total_votes_cast': total_votes,
                'latest_voting_title': latest_voting_title,
                'new_votings_today': new_votings_today
            }
        }
    except Exception as e:
        # Если база данных пуста или произошла ошибка при миграциях
        print(f"Ошибка в context_processor: {e}")
        return {
            'GLOBAL_STATS': {
                'total_users': 0,
                'total_votings': 0,
                'total_votes_cast': 0,
                'latest_voting_title': 'Ошибка загрузки',
                'new_votings_today': 0
            }
        }