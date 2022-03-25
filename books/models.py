from django.db import models
from django.urls import reverse
import datetime
from django.contrib.auth import get_user_model
User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    author = models.CharField(max_length=100, verbose_name='Автор')
    year = models.IntegerField(verbose_name='Год издания', default=datetime.datetime.now().year)
    description = models.TextField(verbose_name='Описание')
    language = models.CharField(max_length=50, verbose_name='Язык')
    original_language = models.CharField(max_length=50, verbose_name='Оригинал')
    pages = models.IntegerField(verbose_name='Количество страниц', default=0)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Обложка')
    price = models.DecimalField(verbose_name='Стоимость', default=0.0, max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    rating = models.FloatField(verbose_name='Рейтинг', default=0.0, blank=True)

    # связь для таблиц Book и Category
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    # def get_rating(self):
    #     # считает рейтинг книги
    #     return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_absolute_url(self):
        return reverse('view_book', kwargs={'pk': self.pk})

    def get_author_url(self):
        return reverse('author', kwargs={'author': self.author})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


class Category(models.Model):
    # db_index устанавливает индекс для поля для ускорения поиска по объектам

    title = models.CharField(max_length=50, db_index=True, verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Comment(models.Model):
    book = models.ForeignKey(Book, verbose_name='Книга', on_delete=models.PROTECT, related_name='comments', null=True)
    user = models.ForeignKey(User,  verbose_name='Пользователь', on_delete=models.PROTECT, related_name='user_comments', null=True)
    body = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)
    active = models.BooleanField(default=True)
    rating = models.IntegerField(verbose_name='Оценка', blank=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return 'Комментарий от {} на книгу {}'.format(self.user, self.book)
