from django import forms
from .models import Order

CITY_CHOICES = (
    ('Минск', 'Минск'),
    ('Брест', 'Брест'),
    ('Витебск', 'Витебск'),
    ('Гомель', 'Гомель'),
    ('Гродно', 'Гродно'),
    ('Могилев', 'Могилев'),
)

PAID_CHOICES = (
    ('Наличными курьеру', 'Наличными курьеру'),
    ('Картой курьеру', 'Картой курьеру'),
)


class OrderCreateForm(forms.ModelForm):
    city = forms.TypedChoiceField(label='Город',
                                  choices=CITY_CHOICES,
                                  coerce=str,
                                  widget=forms.Select(attrs={'class': 'form-select'}))

    street = forms.CharField(label='Улица',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    house = forms.CharField(label='Дом',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    flat = forms.CharField(label='Квартира', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '-'}))
    phone_number = forms.CharField(label='Контактный номер телефона',
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    paid_by = forms.TypedChoiceField(label='Способ оплаты',
                                     choices=PAID_CHOICES,
                                     coerce=str)
    name = forms.CharField(label='Имя',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control'})
                           )
    surname = forms.CharField(label='Фамилия',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control'})
                              )

    class Meta:
        model = Order
        fields = ['city', 'paid_by', 'street', 'house', 'flat', 'phone_number', 'name', 'surname']
