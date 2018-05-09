from django.shortcuts import render
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from news.models import New
from generic.mixins import CategoryListMixin, PageNumberMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from generic.controllers import PageNumberView


# Список новостей
class NewsListView(ArchiveIndexView, CategoryListMixin):
    model = New
    date_field = 'posted'
    template_name = 'news_index.html'
    paginate_by = 10
    allow_empty = True
    allow_future = True


# Отдельная новость
class NewDetailView(DetailView, PageNumberMixin):
    model = New
    template_name = 'new.html'


# Создание новаости
class NewCreate(SuccessMessageMixin, CreateView, CategoryListMixin):
    model = New
    fields = '__all__'
    template_name = 'new_add.html'
    success_url = reverse_lazy('news_index')
    success_message = 'Новость успешно создана'


# Редактирование новости
class NewUpdate(SuccessMessageMixin, PageNumberView, UpdateView, PageNumberMixin):
    model = New
    fields = '__all__'
    template_name = 'new_edit.html'
    success_url = reverse_lazy('news_index')
    success_message = 'Новость успешно изменена'


# Удаление новости
class NewDelete(PageNumberView, DeleteView, PageNumberMixin):
    model = New
    fields = '__all__'
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_index')

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Новость успешно удалена')
        return super().post(request, *args, **kwargs)
