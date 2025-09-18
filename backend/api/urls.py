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
from .views import existing_tag_view, new_tag_view
from .views import existing_imagetag_view, new_imagetag_view

app_name = 'api'
urlpatterns = [
    path('user/', AppUserListView.as_view()),
    path('user/<uuid:user_id>', user_view),
    
    path('image/', ImageListView.as_view()),
    path('image/<uuid:image_id>', image_view),

    path('tag/', TagListView.as_view()),
    path('tag/<uuid:tag_id>', existing_tag_view),
    path('tag/new', new_tag_view),

    path('image-tag/', ImageTagListView.as_view()),
    path('image-tag/<uuid:imagetag_id>', existing_imagetag_view),
    path('image-tag/new', new_imagetag_view)
]
