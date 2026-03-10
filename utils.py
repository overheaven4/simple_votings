import csv
from django.http import HttpResponse
from .models import Voting, VotingOption, Vote
from django.utils import timezone


def export_voting_results_to_csv(voting_id):
    """
    Генерирует CSV файл с результатами конкретного голосования.
    Полезно для администраторов и создателей опросов.
    """
    try:
        voting = Voting.objects.get(id=voting_id)
    except Voting.DoesNotExist:
        return None

    # Создаем объект HttpResponse с правильными заголовками для CSV
    current_date = timezone.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"voting_{voting_id}_results_{current_date}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Создаем writer
    writer = csv.writer(response, delimiter=';', quotechar='"')

    # Записываем заголовок файла (информация об опросе)
    writer.writerow(['ID Голосования', 'Название', 'Дата создания', 'Создатель'])
    writer.writerow([voting.id, voting.title, voting.created_at, voting.creator.username])
    writer.writerow([])  # Пустая строка для разделения

    # Записываем заголовки для результатов
    writer.writerow(['Вариант ответа', 'Количество голосов', 'Процент'])

    options = VotingOption.objects.filter(voting=voting)
    total_votes = Vote.objects.filter(option__in=options).count()

    for option in options:
        option_votes = Vote.objects.filter(option=option).count()
        percentage = (option_votes / total_votes * 100) if total_votes > 0 else 0

        writer.writerow([
            option.text,
            option_votes,
            f"{percentage:.2f}%"
        ])

    writer.writerow([])
    writer.writerow(['Итого голосов:', total_votes, '100%'])

    return response