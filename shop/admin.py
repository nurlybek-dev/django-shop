from django.contrib import admin
from .models import Category, Product, Cart, Order, OrderProduct, Review


class ReviewAdminInline(admin.TabularInline):
    model = Review
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewAdminInline]


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['order_time']
    inlines = [OrderProductInline,]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
