from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Voting, VotingOption, Vote
import random


class Command(BaseCommand):
    help = 'Генерирует тестовые данные для голосований (пользователи, опросы, голоса)'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Количество юзеров')
        parser.add_argument('--votings', type=int, default=5, help='Количество голосований')

    def handle(self, *args, **kwargs):
        users_count = kwargs['users']
        votings_count = kwargs['votings']

        self.stdout.write('Создание пользователей...')
        users = []
        for i in range(users_count):
            user, created = User.objects.get_or_create(
                username=f'testuser_{i}',
                defaults={'email': f'test{i}@example.com'}
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        self.stdout.write('Создание голосований...')
        for i in range(votings_count):
            creator = random.choice(users)
            voting = Voting.objects.create(
                title=f'Тестовое голосование {i}',
                description=f'Описание тестового голосования номер {i}',
                creator=creator
            )

            # Создаем от 2 до 5 вариантов ответа
            for j in range(random.randint(2, 5)):
                VotingOption.objects.create(
                    voting=voting,
                    text=f'Вариант ответа {j}'
                )

        self.stdout.write(self.style.SUCCESS('Успешно сгенерированы тестовые данные!'))