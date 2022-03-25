from django import forms
from .models import Comment

RATING_CHOICES = (
    (5, 5),
    (4, 4),
    (3, 3),
    (2, 2),
    (1, 1),
)


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 5,
        'cols': 20,
        'margin': 0,
    }))

    rating = forms.ChoiceField(label='Оценка',
                               required=False,
                               choices=RATING_CHOICES,
                               widget=forms.Select(attrs={
                                   'style': 'width: auto',
                                   'class': 'form-select',
                               }))

    class Meta:
        model = Comment
        fields = ('body', 'rating')
