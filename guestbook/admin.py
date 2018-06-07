from django.contrib import admin
from guestbook.models import Guestbook


class GuestbookAdmin(admin.ModelAdmin):
    # def get_formatted_datetime(self):
    #     return str(self.posted.day) + '.' + str(self.posted.month) + '.' + str(
    #         self.posted.year) + ' ' + str(self.posted.hour) + ':' + str(
    #         self.posted.minute) + ':' + str(self.posted.second)
    # get_formatted_datetime.short_description = 'Опубликовано'

    list_display = ('posted', 'user', 'content')  # список полей, отображаемых в таблице записей
    list_display_links = ('posted', 'user')  # на каких полях будет гиперссылка на запись
    list_per_page = 50  # количество записей на 1-й странице
    search_fields = ('user', 'content')  # добавление на страницу строки поиска и указание полей, по которым будет идти фильтрация
    date_hierarchy = 'posted'  # указание поля с типом дата/время для вывода вверху страницы ссылок фильтрации по датам
    list_filter = ('user', )  # добавить фильтр по значениям указанных полей
    preserve_filters = False  # сброс заданной фильтрации при добавлении/редактировании/удалении записи
    ordering = ('user', 'posted')  # сортировка отображаемых данных
    # list_editable = ('content',)  # поля, которые можно редактировать прямо на этой странице
    # actions_on_bottom = True  # отобразить список действий внизу страницы
    # exclude = ('user', )  # не отображать указанные поля при редактировании
    # readonly_fields = ('user', )  # вывод поля в виде 'только для чтения'


admin.site.register(Guestbook, GuestbookAdmin)
