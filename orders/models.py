from django.db import models
from books.models import Book

from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Заказ принят')
    updated = models.DateTimeField(auto_now=True, verbose_name='Заказ обновлен')
    paid_by = models.CharField(max_length=50, verbose_name='Способ оплаты')
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.PROTECT, null=True,
                             verbose_name='Пользователь')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ №{}'.format(self.pk)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    book = models.ForeignKey(Book, related_name='order_items', on_delete=models.PROTECT, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return 'Товар №{}'.format(self.pk)

    def get_cost(self):
        return self.price * self.quantity
