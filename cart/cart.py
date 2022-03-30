from decimal import Decimal
from django.conf import settings
from books.models import Book


class Cart(object):

    def __init__(self, request):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем ПУСТУЮ корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Перебираем товары в корзине и получаем товары из базы данных.
        """
        book_ids = self.cart.keys()
        # получаем товары и добавляем их в корзину
        books = Book.objects.filter(id__in=book_ids)

        cart = self.cart.copy()
        for book in books:
            cart[str(book.id)]['book'] = book

        for item in cart.values().__reversed__():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

        # Yield — это ключевое слово в Python, которое используется для возврата из функции с сохранением
        # состояния ее локальных переменных, и при повторном вызове такой функции выполнение продолжается
        # с оператора yield, на котором ее работа была прервана. Любая функция, содержащая ключевое слово
        # yield, называется генератором.

    def __len__(self):
        """
        Считаем сколько товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, book, quantity=1, update_quantity=False):
        """
        Добавляем товар в корзину или обновляем его количество.
        """
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 0,
                                  'price': str(book.price)}
        if update_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity
        self.save()

    def save(self):
        # сохраняем товар
        self.session.modified = True

    def remove(self, book):
        """
        Удаляем товар
        """
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def get_total_price(self):
        # получаем общую стоимость
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # очищаем корзину в сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()
