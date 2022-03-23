from django import forms

BOOK_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddBookForm(forms.Form):
    quantity = forms.TypedChoiceField(
        label='',
        choices=BOOK_QUANTITY_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'margin-bottom: 10px'})
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )