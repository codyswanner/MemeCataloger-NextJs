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
from django.http import HttpResponse
# noinspection PyUnresolvedReferences
from django.db.models.query import QuerySet  # for TypeHints


# Create your views here.
class AppUserListView(generics.ListCreateAPIView):
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


class ImageListView(generics.ListAPIView):
    """ImageView
    Exposes API-delivered Image information.
    See api.models.Image for details.
    """

    queryset: QuerySet = Image.objects.all()
    serializer_class = ImageSerializer
    renderer_classes = [JSONRenderer]


class TagListView(generics.ListAPIView):
    """TagView
    Exposes API-delivered Tag information.
    See api.models.Tag for details.
    """

    queryset: QuerySet = Tag.objects.all()
    serializer_class = TagSerializer
    renderer_classes = [JSONRenderer]


class ImageTagListView(generics.ListAPIView):
    """ImageTagView
    Exposes API-delivered ImageTag information.
    See api.models.ImageTag for details.
    """

    queryset: QuerySet = ImageTag.objects.all()
    serializer_class = ImageTagSerializer
    renderer_classes = [JSONRenderer]


def user_view(_, **user_id):
    return HttpResponse(
        "<div>You landed on the user view!</div>"
        f"<div>The user id is: {user_id}</div>"
        "<div>This page hasn't really been implemented for anything yet.</div>"
    )

def image_view(_, **image_id):
    requested_image: Image = Image.objects.get(id=image_id['image_id'])

    return HttpResponse(
        requested_image.source,
        content_type="image/png"
    )

def existing_tag_view(request, tag_id):
    ...
    return HttpResponse(status=503)

def new_tag_view(request):
    ...
    return HttpResponse(status=503)

def existing_imagetag_view(request, imagetag_id):
    ...
    return HttpResponse(status=503)

def new_imagetag_view(request):
    ...
    return HttpResponse(status=503)
