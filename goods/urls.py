from django.contrib.auth.decorators import permission_required
from django.urls import re_path
from goods.views import GoodListView, GoodDetailView, GoodCreate, GoodUpdate, GoodDelete

urlpatterns = [
    re_path(r'^(?P<pk>\d+)/$', GoodListView.as_view(), name='goods_index'),
    re_path(r'^(?P<pk>\d+)/detail/$', GoodDetailView.as_view(), name='goods_detail'),
    re_path(r'^(?P<pk>\d+)/add/$', permission_required('goods.add_good')(GoodCreate.as_view()), name='goods_add'),
    re_path(r'^(?P<pk>\d+)/edit/$', permission_required('goods.change_good')(GoodUpdate.as_view()), name='goods_edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', permission_required('goods.delete_good')(GoodDelete.as_view()), name='goods_delete'),

]