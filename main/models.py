from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Voting(models.Model):
    """Модель для хранения информации о голосовании"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)


class VotingOption(models.Model):
    """Модель для хранения информации о варианте голосования"""
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)


class Vote(models.Model):
    """Модель для хранения информации о голосе пользователя"""
    option = models.ForeignKey(to=VotingOption, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)