from django.contrib import admin
from .models import Category, Product, Client, Order


def increase_product_stock(request, queryset):
    for qs in queryset:
        qs.stock += 50
        qs.save()


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = [increase_product_stock]

    class Meta:
        model = Product


def interested_in(obj):
    categories = obj.interested_in.all()
    return [category.name for category in categories]


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', interested_in)
    interested_in.short_description = 'Interested in'

    class Meta:
        model = Client


# Register your models here.


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order)
