"""Defines views for the app.
    Informational views give a clear look at data such as Users,
    Images, Tags, and ImageTags.

Classes
-------
[class]View
    Exposes API-delivered [class] information.
    For example, ImageView exposes data from class api.models.Image.
    Includes: AppUserView, ImageView, TagView, ImageTagView.

"""

# from django.http import HttpResponse
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from .models import AppUser, Image, Tag, ImageTag
from .serializers import \
    AppUserSerializer, ImageSerializer, TagSerializer, ImageTagSerializer
# noinspection PyUnresolvedReferences
from django.db.models.query import QuerySet  # for TypeHints


# Create your views here.
class AppUserView(generics.ListCreateAPIView):
    """AppUserView
    Exposes API-delivered AppUser information.
    See api.models.AppUser for details.
    """

    queryset: QuerySet = AppUser.objects.all()
    serializer_class = AppUserSerializer
    renderer_classes = [JSONRenderer]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"message": "User created successfully."}
        return response


class ImageView(generics.ListAPIView):
    """ImageView
    Exposes API-delivered Image information.
    See api.models.Image for details.
    """

    queryset: QuerySet = Image.objects.all()
    serializer_class = ImageSerializer
    renderer_classes = [JSONRenderer]


class TagView(generics.ListAPIView):
    """TagView
    Exposes API-delivered Tag information.
    See api.models.Tag for details.
    """

    queryset: QuerySet = Tag.objects.all()
    serializer_class = TagSerializer
    renderer_classes = [JSONRenderer]


class ImageTagView(generics.ListAPIView):
    """ImageTagView
    Exposes API-delivered ImageTag information.
    See api.models.ImageTag for details.
    """

    queryset: QuerySet = ImageTag.objects.all()
    serializer_class = ImageTagSerializer
    renderer_classes = [JSONRenderer]
