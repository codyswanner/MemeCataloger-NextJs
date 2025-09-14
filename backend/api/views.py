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

import json
from uuid import UUID
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


def user_view(_, **user_id) -> HttpResponse:
    return HttpResponse(
        "<div>You landed on the user view!</div>"
        f"<div>The user id is: {user_id}</div>"
        "<div>This page hasn't really been implemented for anything yet.</div>"
    )

def image_view(_, **image_id) -> HttpResponse:
    requested_image: Image = Image.objects.get(id=image_id['image_id'])

    return HttpResponse(
        requested_image.source,
        content_type="image/png"
    )

def existing_tag_view(request, tag_id) -> HttpResponse:
    """Handles requests meant to manipulate existing Tag objects.
    Accepts the following methods:

    GET: return details of the Tag object specified by request.tag_id.
    POST: update the name of the Tag object specified by request.tag_id.
    DELETE: deletes the Tag object specified by request.tag_id.

    request.tag_id is supplied by a matching pattern in the URL;
    see api.urls module and https://docs.djangoproject.com/en/5.2/topics/http/urls/
    for more information.
    """

    # validate that request is either GET, PUT or DELETE
    if request.method not in ["GET", "PUT", "DELETE"]:
        return HttpResponse(
            status=405,
            content="This resource requires GET, PUT or DELETE method."
        )
    
    # validate user is signed in, and request user-id matches
    ...

    # validate user owns specified resource
    ...

    # respond to GET requests with details of Tag object
    if request.method == "GET":
        try:
            target_tag: Tag = Tag.objects.get(id=tag_id)
            response_data = {
                "tag-id": f"{target_tag.id}",
                "tag-name": f"{target_tag.name}",
                "tag-owner": f"{target_tag.owner.id}"
            }
            return HttpResponse(
                status=200,
                content=json.dumps(response_data)
            )
        except Tag.DoesNotExist:
            return HttpResponse(status=400)

    # carry out DELETE requests and confirm to client
    if request.method == "DELETE":
        # validate request properly formed
        try:
            target_tag: Tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return HttpResponse(status=400)

        # carry out deletion
        target_tag.delete()
        response_data: dict = {"tag-id": f"{tag_id}"}
        return HttpResponse(
            status=200,
            content=json.dumps(response_data)
        )

    # validate PUT request is properly formed
    try:
        target_tag: Tag = Tag.objects.get(id=tag_id)
        request_data = json.loads(request.body)
        new_tag_name: str = request_data['tag-name']
    except (Tag.DoesNotExist, KeyError):
        return HttpResponse(status=400)

    # update tag name as specified
    target_tag.name = new_tag_name
    target_tag.save()
    response_data = {
        "tag-id": f"{tag_id}",
        "tag-name": f"{target_tag.name}"
    }

    return HttpResponse(
        status=200,
        content=json.dumps(response_data)
    )

def new_tag_view(request) -> HttpResponse:
    """Handles requests to create a new Tag object.
    Accepts the following methods:

    GET: return required details for creating a new Tag object.
    POST: create a new Tag object with given tag-name and owner by user-id.
    """

    # validate method is GET or POST
    if request.method not in ["GET", "POST"]:
        return HttpResponse(
            status=405,
            content="This resource requires GET or POST method."
        )

    # validate user is signed in, and request user-id matches
    ...

    # respond to GET requests with details required to create Tag object
    if request.method == "GET":
        return HttpResponse(
            "Requires POST request with data:" \
            "{" \
            "  user-id: uuid of resource owner," \
            "  tag-name: string name to give specified tag" \
            "}"
        )
    
    # validate request is properly formed
    try:
        tag_name:str = request.POST['tag-name']
        user_id: UUID = request.POST['user-id']
        requesting_user: AppUser = AppUser.objects.get(id=user_id)
    except (KeyError, AppUser.DoesNotExist):
        return HttpResponse(
            status=400,
            content="Requires POST request with data:" \
            "{" \
            "  user-id: uuid of resource owner," \
            "  tag-name: string name to give specified tag" \
            "}"
        )
    
    # if passed all checks, create Tag as specified
    new_tag: Tag = Tag.objects.create(owner=requesting_user, name=tag_name)
    new_tag.save()
    response_data = {
        "tag-id": f"{new_tag.id}",
        "tag-name": new_tag.name
    }

    return HttpResponse(
        status=200,
        content=json.dumps(response_data)
    )

def existing_imagetag_view(request, imagetag_id):
    ...
    return HttpResponse(status=503)

def new_imagetag_view(request):
    ...
    return HttpResponse(status=503)
