from django.shortcuts import render
from django.forms.models import modelformset_factory
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView

from categories.models import Category
from generic.mixins import CategoryListMixin

CategoriesFormset = modelformset_factory(Category, fields=('name', 'order'), can_delete=True)


class CategoriesEdit(TemplateView, CategoryListMixin):
    template_name = 'categories_edit.html'
    formset = None

    def get(self, request, *args, **kwargs):
        self.formset = CategoriesFormset()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        self.formset = CategoriesFormset(request.POST)
        if self.formset.is_valid():
            self.formset.save()
            messages.add_message(request, messages.SUCCESS, 'Список категорий успешно изменен')
            return redirect('categories_edit')
