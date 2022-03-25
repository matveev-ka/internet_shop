from django.contrib import admin
from django.forms import TextInput, Textarea
from django import forms
from .models import *
from django.utils.safestring import mark_safe
from django.db import models


class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 150})},
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 150})},
    }
    list_display = (
        'id', 'title', 'author', 'year', 'language', 'original_language', 'pages', 'get_image', 'price', 'created_at',
        'available', 'rating',
    )
    list_display_links = ('id', 'title')
    search_fields = ('id', )  # поиск по артикулу
    list_filter = ('year', 'category')
    fields = (
        'title', 'author', 'year', 'description', 'language', 'original_language', 'pages', 'image', 'price',
        'category', 'available')
    readonly_fields = ('get_image', 'created_at', 'rating')
    save_on_top = True
    empty_value_display = '-пусто-'

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150">')

    get_image.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'book')
    ordering = ['-created']


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.site_title = 'Управление каталогом'
admin.site.site_header = 'Управление каталогом'
