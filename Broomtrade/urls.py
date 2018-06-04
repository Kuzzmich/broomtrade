"""Broomtrade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth.views import login as login_view
from django.contrib.auth.views import logout as logout_view
from django.conf import settings
from django.conf.urls.static import static
from about.views import AboutView
from contacts.views import ContactsView
from howtobuy.views import HowToBuyView
from news.views import RssNewsListFeed, AtomNewsListFeed
from goods.views import RssGoodListFeed, AtomGoodsListFeed

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'login/', login_view, name='login'),
    re_path(r'logout/', logout_view, name='logout'),
    re_path(r'^', include('main.urls')),
    re_path(r'^guestbook/', include('guestbook.urls')),
    re_path(r'^news/', include('news.urls')),
    re_path(r'^imagepool/', include('imagepool.urls')),
    re_path(r'^categories/', include('categories.urls')),
    re_path(r'goods/', include('goods.urls')),
    re_path(r'comment/', include('django_comments.urls')),
    re_path(r'^blog/', include('blog.urls')),
    re_path(r'^about/', AboutView.as_view(), name='about'),
    re_path(r'^contacts/', ContactsView.as_view(), name='contacts'),
    re_path(r'^howtobuy/', HowToBuyView.as_view(), name='howtobuy'),
    re_path(r'^feed/rss/', RssNewsListFeed(), name='news_feed_rss'),
    re_path(r'^feed/atom/', AtomNewsListFeed(), name='news_feed_atom'),
    re_path(r'^(?P<pk>\d+)/feed/rss/', RssGoodListFeed(), name='goods_feed_rss'),
    re_path(r'^(?P<pk>\d+)/feed/atom/', AtomGoodsListFeed(), name='goods_feed_atom')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
