from django import template

register = template.Library()


@register.filter
def user_data(value, arg):
    """Заменяет данные из формы заказа на данные пользователя, если они есть"""
    value = arg
    return value
