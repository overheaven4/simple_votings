import logging
import os
from django.conf import settings
from django.utils import timezone


def setup_app_logger(logger_name='voting_app'):
    """
    Создает и настраивает кастомный логгер для записи важных
    событий платформы (создание опросов, подозрительная активность).
    """
    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(levelname)s[%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Пытаемся создать директорию logs, если её нет
    log_dir = os.path.join(settings.BASE_DIR, 'logs')
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, 'platform_activity.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        # Fallback (запасной вариант): выводим в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.warning(f"Не удалось создать файл логов: {e}")

    return logger


# Глобальный объект логгера для импорта в другие файлы
app_logger = setup_app_logger()


def log_vote_event(user, voting, option):
    """Хелпер для быстрого логирования голоса"""
    app_logger.info(
        f"Голосование | Юзер: {user.username} (ID:{user.id}) | "
        f"Опрос: {voting.id} | Выбрал: '{option.text}'"
    )