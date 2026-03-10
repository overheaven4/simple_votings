from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from main.models import Voting, Vote
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Voting)
def notify_new_voting(sender, instance, created, **kwargs):
    """
    Сигнал: срабатывает при создании нового голосования в БД.
    """
    if created:
        message = f"SYSTEM: Новое голосование создано: '{instance.title}' (Автор: {instance.creator.username})"
        print(message)
        logger.info(message)
        # Здесь в будущем можно подключить Celery задачу на email рассылку:
        # send_notifications_task.delay(instance.id)


@receiver(post_save, sender=Vote)
def check_voting_milestones(sender, instance, created, **kwargs):
    """
    Сигнал: проверяет достижение круглого количества голосов.
    """
    if created:
        voting = instance.option.voting
        total_votes = Vote.objects.filter(option__voting=voting).count()

        # Триггер на "популярный опрос"
        if total_votes in [10, 50, 100, 500]:
            print(f"MILESTONE: Голосование '{voting.title}' набрало {total_votes} голосов!")
            logger.info(f"Voting ID {voting.id} reached {total_votes} votes milestone.")


@receiver(pre_delete, sender=Voting)
def backup_voting_data(sender, instance, **kwargs):
    """
    Сигнал: Логирует предупреждение перед удалением опроса.
    """
    logger.warning(f"ОПАСНОСТЬ: Голосование '{instance.title}' сейчас будет удалено из базы данных!")