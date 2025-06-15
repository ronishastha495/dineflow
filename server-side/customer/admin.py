from django.contrib import admin
from .models import Order, Review

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'item', 'quantity', 'ordered_at')
    list_filter = ('ordered_at',)
    search_fields = ('customer__username', 'item__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'item', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('customer__username', 'item__name', 'comment')
