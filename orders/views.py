from django.contrib import messages
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth import get_user_model

User = get_user_model()


def order_create(request):
    """Оформление заказа"""
    cart = Cart(request)
    data = {
        'name': request.user.name,
        'surname': request.user.surname,
        'phone_number': request.user.phone_number,
        'street': request.user.street,
        'house': request.user.house,
        'flat': request.user.flat,
    }
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            request.user.phone_number = form.cleaned_data['phone_number']
            request.user.name = form.cleaned_data['name']
            request.user.surname = form.cleaned_data['surname']
            request.user.street = form.cleaned_data['street']
            request.user.house = form.cleaned_data['house']
            request.user.flat = form.cleaned_data['flat']
            request.user.save()

            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         book=item['book'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            messages.success(request, 'Ваш заказ был принят. Номер вашего заказа: ' + str(
                order.id) + ' (история заказов в личном кабинете).')
            return redirect('home')
        else:
            messages.error(request, 'Проверьте правильность введенных данных')
    else:
        form = OrderCreateForm(data)
    return render(request, 'orders/create.html',
                  {'cart': cart, 'form': form})
