from django.core.exceptions import ValidationError
import re


def validate_voting_title(value):
    """
    Проверяет, что название голосования не слишком короткое
    и не содержит запрещенных символов (например, HTML тегов).
    """
    if len(value.strip()) < 5:
        raise ValidationError(
            'Название голосования должно содержать минимум 5 символов.',
            params={'value': value},
        )

    # Запрещаем HTML-теги для защиты от XSS атак
    if re.search(r'<[^>]*>', value):
        raise ValidationError(
            'HTML-теги и спецсимволы в названии запрещены в целях безопасности.',
            params={'value': value},
        )


def validate_options_count(options_list):
    """
    Проверяет, что при создании передано корректное количество вариантов ответа,
    а также нет пустых строк или полных дубликатов.
    """
    # Очищаем от пустых строк и пробелов
    valid_options = [str(opt).strip() for opt in options_list if str(opt).strip()]

    if len(valid_options) < 2:
        raise ValidationError(
            'Любое голосование должно содержать как минимум 2 варианта ответа.'
        )

    if len(valid_options) > 15:
        raise ValidationError(
            'Голосование не может содержать более 15 вариантов ответа.'
        )

    # Проверка на дубликаты (сравниваем длину списка с множеством)
    if len(valid_options) != len(set(valid_options)):
        raise ValidationError(
            'Варианты ответа в одном голосовании не должны повторяться.'
        )