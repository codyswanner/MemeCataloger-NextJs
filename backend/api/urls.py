"""Registers package URLs to the Django app.

The following URLs provide API-delivered data:
 - user/
 - image/
 - tag/
 - image-tag/
"""

from django.urls import path
from .views import AppUserView, ImageView, TagView, ImageTagView

app_name = 'api'
urlpatterns = [
    path('user/', AppUserView.as_view()),
    path('image/', ImageView.as_view()),
    path('tag/', TagView.as_view()),
    path('image-tag/', ImageTagView.as_view())
]