from catalog.models import Product


def get_products_by_category(category_id, user=None):
    """Функция, возвращающая продукты, отфильтрованные по категории и правам пользователя"""
    queryset = Product.objects.filter(category_id=category_id)
    return filter_products_for_user(queryset, user)


def filter_products_for_user(queryset, user):
    """Функция, возвращающая queryset, отфильтрованный по правам пользователя"""
    if user and not user.has_perm('catalog.can_unpublish_product'):
        return queryset.filter(status='published')
    return queryset
