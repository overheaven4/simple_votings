import logging
from django.utils import timezone
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class UserActivityAnalyticsMiddleware:
    """
    Middleware для отслеживания активности пользователей
    и логирования времени их последнего запроса к платформе.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Код, выполняемый до вызова view (до обработки запроса)
        if hasattr(request, 'user') and request.user.is_authenticated:
            self.log_user_activity(request.user, request.path, request.method)

        response = self.get_response(request)

        # Код, выполняемый после вызова view
        # Можно добавить дополнительные заголовки в response
        response['X-Platform-Version'] = '1.0.0'
        return response

    def log_user_activity(self, user, path, method):
        """
        Логирует информацию о действиях пользователя.
        В реальном высоконагруженном проекте пишется в Redis или брокер сообщений.
        """
        current_time = timezone.now()
        log_message = f"User {user.username} (ID: {user.id}) accessed {path} [{method}] at {current_time}"

        # Вывод в консоль для отладки
        print(f"[ACTIVITY LOG] {log_message}")

        # Логирование через стандартный модуль logging
        logger.info(log_message)