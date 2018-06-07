from django.contrib import admin
from categories.models import Category
from goods.models import Good


# class GoodInline(admin.StackedInline):
#     model = Good
#     fields = (
#         'name',
#         'description',
#         'content',
#         ('price', 'price_acc'),
#         ('in_stock', 'featured'),
#         'image',
#     )  # форма добавления товара в категорию


class CategoryAdmin(admin.ModelAdmin):
    fields = (('name', 'order'),)
    # inlines = (GoodInline,)  # Размещение формы добавления товара в категорию (поля ввода друг под другом)

admin.site.register(Category, CategoryAdmin)
