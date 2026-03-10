from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_paginated_data(request, queryset, items_per_page=10, page_param='page'):
    """
    Утилита для пагинации любого QuerySet'а в функциональных представлениях (FBV).
    Обеспечивает безопасную обработку неверных номеров страниц
    и генерирует красивый диапазон кнопок для шаблона.
    """
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get(page_param)

    try:
        # Пытаемся получить запрошенную страницу
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Если параметр страницы не является числом, отдаем первую страницу
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # Если номер страницы больше, чем количество страниц, отдаем последнюю
        page_obj = paginator.get_page(paginator.num_pages)

    # Генерируем список страниц для красивого отображения в шаблоне
    current = page_obj.number
    total = paginator.num_pages

    # Логика: показываем 5 кнопок (например: 1 2 [3] 4 5 или 7 8 [9] 10 11)
    if total <= 5:
        page_range = range(1, total + 1)
    elif current <= 3:
        page_range = range(1, 6)
    elif current >= total - 2:
        page_range = range(total - 4, total + 1)
    else:
        page_range = range(current - 2, current + 3)

    return {
        'page_obj': page_obj,
        'items': page_obj.object_list,
        'is_paginated': total > 1,
        'page_range': page_range,
        'total_items': paginator.count,
        'current_page': current,
        'total_pages': total
    }