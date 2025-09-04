"""Registers package URLs to the Django app.

The following URLs provide API-delivered data:
 - user/
 - image/
 - tag/
 - image-tag/
"""

from django.urls import path
from .views import AppUserListView, ImageListView, TagListView, ImageTagListView
from .views import user_view, image_view

app_name = 'api'
urlpatterns = [
    path('user/', AppUserListView.as_view()),
    path('user/<uuid:user_id>', user_view),
    path('image/', ImageListView.as_view()),
    path('image/<uuid:image_id>', image_view),
    path('tag/', TagListView.as_view()),
    path('image-tag/', ImageTagListView.as_view())
]