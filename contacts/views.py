from django.shortcuts import render
from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from contacts.models import MailList


class ContactsView(SuccessMessageMixin, CreateView, CategoryListMixin):
    model = MailList
    fields = '__all__'
    template_name = 'contacts.html'
    success_url = reverse_lazy('contacts')
    success_message = 'Вы успешно добавлены в список рассылки'
