import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_votings.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import Voting, VotingOption, Vote

# Создаём пользователей
alice = User.objects.create_user(username='alice', email='alice@example.com', password='alicepass')
bob = User.objects.create_user(username='bob', email='bob@example.com', password='bobpass')

# Голосование
voting = Voting.objects.create(
    title="Любимый цвет",
    description="Выберите свой любимый цвет",
    creator=alice,
    created_at=timezone.now()
)



# Варианты
red = VotingOption.objects.create(voting=voting, text="Красный")
blue = VotingOption.objects.create(voting=voting, text="Синий")
green = VotingOption.objects.create(voting=voting, text="Зелёный")

# Голоса
Vote.objects.create(option=red, user=alice)
Vote.objects.create(option=blue, user=bob)

print("Тестовые данные созданы!")