from django.shortcuts import render
from django.views.generic.base import ContextMixin
from django.views.generic.list import ListView
from generic.mixins import CategoryListMixin
from goods.models import Category
from goods.models import Good
from generic.controllers import PageNumberView

from django.views.generic.detail import DetailView
from generic.mixins import PageNumberMixin

from django.views.generic.base import TemplateView
from django.forms.models import inlineformset_factory
from goods.models import GoodImage
from goods.forms import GoodForm, GoodImageForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from django.views.generic.edit import DeleteView

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.exceptions import ObjectDoesNotExist

import logging


# Сортировка товаров
class SortMixin(ContextMixin):
    sort = '0'
    order = 'A'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.sort
        context['order'] = self.order
        return context


# Список товаров
logger = logging.getLogger(__name__)


class GoodListView(PageNumberView, ListView, SortMixin, CategoryListMixin):
    model = Good
    template_name = 'goods_index.html'
    paginate_by = 2
    cat = None

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=self.kwargs['pk'])
        # logger.debug(self.cat.name)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.cat
        return context

    def get_queryset(self):
        goods = Good.objects.filter(category=self.cat)

        # Сортировка столбцов
        if self.sort == '2':
            if self.order == 'D':
                goods = goods.order_by('-in_stock', 'name')
            else:
                goods = goods.order_by('in_stock', 'name')
        elif self.sort == '1':
            if self.order == 'D':
                goods = goods.order_by('-price', 'name')
            else:
                goods = goods.order_by('price', 'name')
        else:
            if self.order == 'D':
                goods = goods.order_by('-name')
            else:
                goods = goods.order_by('name')
        return goods


# Страница товара
class GoodDetailView(PageNumberView, DetailView, SortMixin, PageNumberMixin):
    model = Good
    template_name = 'good.html'


GoodImageFormset = inlineformset_factory(Good, GoodImage, fields='__all__', can_order=True)


# Создание товара
class GoodCreate(PageNumberView, TemplateView, SortMixin, PageNumberMixin):
    template_name = 'good_add.html'
    cat = None
    form = None
    formset = None

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=self.kwargs['pk'])
        self.form = GoodForm(initial={'category': self.cat})
        self.formset = GoodImageFormset()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.cat
        context['form'] = self.form
        context['formset'] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        self.form = GoodForm(request.POST, request.FILES)
        if self.form.is_valid():
            new_good = self.form.save()
            self.formset = GoodImageFormset(request.POST, request.FILES, instance=new_good)
            if self.formset.is_valid():
                self.formset.save()
                messages.add_message(request, messages.SUCCESS, 'Товар успешно добавлен')
                return redirect(reverse('goods_index', kwargs={'pk': new_good.category.pk}) +
                                '?page=' + self.request.GET['page'] +
                                '&sort=' + self.request.GET['sort'] +
                                '&order=' + self.request.GET['order'])
        if self.kwargs['pk'] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=self.kwargs['pk'])
        self.formset = GoodImageFormset(request.POST, request.FILES)
        return super().get(request, *args, **kwargs)


# Редактирвоание товара
class GoodUpdate(PageNumberView, TemplateView, SortMixin, PageNumberMixin):
    good = None
    template_name = 'good_edit.html'
    form = None
    formset = None

    def get(self, request, *args, **kwargs):
        self.good = Good.objects.get(pk=self.kwargs['pk'])
        self.form = GoodForm(instance=self.good)
        self.formset = GoodImageFormset(instance=self.good)
        return super().get(request, *args, *kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['good'] = self.good
        context['form'] = self.form
        context['formset'] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        self.good = Good.objects.get(pk=self.kwargs['pk'])
        self.form = GoodForm(request.POST, request.FILES, instance=self.good)
        self.formset = GoodImageFormset(request.POST, request.FILES, instance=self.good)
        if self.form.is_valid():
            self.form.save()
            if self.formset.is_valid():
                self.formset.save()
                messages.add_message(request, messages.SUCCESS, 'Товар успешно изменен')
                return redirect(reverse('goods_index', kwargs={'pk': self.good.category.pk}) +
                                '?page=' + self.request.GET['page'] +
                                '&sort=' + self.request.GET['sort'] +
                                '&order=' + self.request.GET['order'])
        return super().get(request, *args, **kwargs)


# Удаление товара
class GoodDelete(PageNumberView, DeleteView, SortMixin, PageNumberMixin):
    model = Good
    template_name = 'good_delete.html'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('goods_index',
                                   kwargs={'pk': Good.objects.get(pk=self.kwargs['pk']).category.pk}) + \
                           '?page=' + self.request.GET['page'] + \
                           '&sort=' + self.request.GET['sort'] + \
                           '&order=' + self.request.GET['order']
        messages.add_message(request, messages.SUCCESS, 'Товар успешно удален')
        return super().post(request, *args, **kwargs)


# RSS рассылка
class RssGoodListFeed(Feed):
    def get_object(self, request, *args, **kwargs):
        try:
            return Category.objects.get(pk=kwargs['pk'])
        except Category.DoesNotExist:
            raise ObjectDoesNotExist('Нет такой категории!')

    def title(self, obj):
        return obj.name

    def description(self, obj):
        return 'Товары, относящиеся к категории "' + obj.name + '"'

    def link(self, obj):
        return reverse('goods_index', kwargs={'pk': obj.pk})

    def categories(self, obj):
        return [obj.name]

    def items(self, obj):
        return Good.objects.filter(category=obj).order_by('name')

    def title(self, obj):
        return 'Товары, относящиеся к категории "' + obj.name + '" :: Веник-Торг'

    def description(self, obj):
        return self.title(obj)

    def item_categories(self, item):
        return [item.category.name]

    def item_link(self, item):
        return reverse('goods_detail', kwargs={'pk': item.pk})


class AtomGoodsListFeed(RssGoodListFeed):
    feed_type = Atom1Feed
    subtitle = RssGoodListFeed.description