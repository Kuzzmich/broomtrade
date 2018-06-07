from django.contrib import admin
from goods.models import Good


class GoodAdmin(admin.ModelAdmin):
    # fields = (
    #     ('name', 'category'),
    #     'description',
    #     'content',
    #     ('price', 'price_acc'),
    #     ('in_stock', 'featured'),
    #     'image'
    # )   # отображение указанных полей на странице записи (указанные в скобках поля выводятся в строку)
    radio_fields = {'category': admin.HORIZONTAL}   # представление списка предустановленныех значений в виде радио-кнопок
    save_on_top = True  # отобразить кнопки вверху страницы
    save_as = True  # заменить кнопку "Сохранить и добавить другой объект" на "Сохранить, как новый объект"
    fieldsets = (
        (None, {'fields': (('name', 'category'),)}),
        ('Описание', {'fields': ('description', 'content')}),
        ('Цена', {'fields': (('price', 'price_acc'),)}),
        ('Дополнительные параметры', {
            'classes': ('collapse',),
            'fields': (('in_stock', 'featured'),),
        }),
        ('Изображение', {'fields': ('image',)}),  # группировка полей записи
    )


admin.site.register(Good, GoodAdmin)
