from django import template
from books.models import Category
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe

from orders.models import Order, OrderItem

register = template.Library()


@register.simple_tag()
def get_categories():
    """Возвращает список категорий, где есть хоть одна книга в наличии"""
    return Category.objects.filter(book__available=True).annotate(Count('book')).order_by('title')


@register.filter(needs_autoescape=True)
def get_mark_str(value, arg, autoescape=True):
    """Выделяет текст, который искал пользователь"""
    start = value.lower().find(arg.lower())
    end = start + len(arg)
    if start == -1:
        return mark_safe(value)
    result = '{0}<mark style="padding: 0;">{1}</mark>{2}'.format(value[:start], value[start:end], value[end:])
    return mark_safe(result)


@register.filter
def get_order_url(value):
    """Возвращает поле, по которому нужно делать сортировку"""
    # Не работает в различных категориях
    return reverse('book_ordering', kwargs={'order': value})


@register.filter()
def product_from_order(value):
    """Возвращает товары из заказа"""
    return OrderItem.objects.filter(order=value)
