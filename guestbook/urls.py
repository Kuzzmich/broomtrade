from django.urls import re_path
from guestbook.views import GuestbookView

urlpatterns = [
    re_path(r'^$', GuestbookView.as_view(), name='guestbook')
]