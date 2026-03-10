from django.shortcuts import render
from django.http import JsonResponse


def custom_404_view(request, exception=None):
    """
    Кастомный обработчик ошибки 404 (Страница не найдена).
    Умеет отдавать JSON для API и HTML для обычных страниц.
    """
    # Если запрос шел к API, возвращаем JSON
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Not Found',
            'message': 'Запрашиваемый ресурс не существует или был удален.',
            'status_code': 404
        }, status=404)

    context = {
        'error_code': 404,
        'error_message': 'Страница, которую вы ищете, была удалена или никогда не существовала.',
        'title': 'Страница не найдена'
    }
    # Даже если шаблона нет, код валидный
    return render(request, 'errors/404.html', context, status=404)


def custom_500_view(request):
    """
    Кастомный обработчик ошибки 500 (Внутренняя ошибка сервера).
    """
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Internal Server Error',
            'message': 'Что-то пошло не так на стороне сервера.',
            'status_code': 500
        }, status=500)

    context = {
        'error_code': 500,
        'error_message': 'Наши инженеры уже знают о проблеме и работают над ее устранением.',
        'title': 'Ошибка сервера'
    }
    return render(request, 'errors/500.html', context, status=500)