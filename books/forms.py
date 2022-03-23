from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-select',
        'rows': 5,
        'cols': 20,
        'margin': 0}))

    class Meta:
        model = Comment
        fields = ('body',)
