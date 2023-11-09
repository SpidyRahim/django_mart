from django.contrib import admin
from . models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    # comma disi karon ekta tuple hisebe kaj korate hobe...django bujhe na tai comma rakhte hoy
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ['product_name', 'price', 'category',
                    'stock', 'created_date', 'modified_date', 'is_available']


admin.site.register(Product, ProductAdmin)
