from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'city', 'paid_by', 'created', 'updated']
    list_filter = ['created', 'updated']
    list_display_links = ('id',)
    search_fields = ('id', 'user__email')
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
