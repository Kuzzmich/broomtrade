from django.shortcuts import render
from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin

# TypeError: metaclass conflict: the metaclass of a derived class
# must be a (non-strict) subclass of the metaclasses of all its bases


# class MainPageView(TemplateView, CategoryListMixin):
#     template_name = 'mainpage.html'
class MainPageView(TemplateView):
    template_name = 'mainpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_url'] = self.request.path
        return context
