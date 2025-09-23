"""Tests for Django views in the api package.
Most test classes in this module check their target view for:
  - data validation
  - ownership of specified resource(s)*
  - rejection of disallowed methods
  - correct response to allowed methods
* currently user auth is not implemented, so ownership checks are very basic.
"""

from django.test import Client, TestCase
import json
from api.models import AppUser, Image, Tag, ImageTag


class ExistingTagViewTestCase(TestCase):
  """Tests the existing_tag_view, including GET, PUT, and DELETE methods.
  GET: return details of the Tag object specified by request.tag_id.
  PUT: update the name of the Tag object specified by request.tag_id.
  DELETE: deletes the Tag object specified by request.tag_id.
  """

  @classmethod
  def setUpTestData(cls) -> None:
    cls.test_user: AppUser = AppUser.objects.create(username="test_user_1")
    cls.test_tag: Tag = Tag.objects.create(
      name="test_tag",
      owner=cls.test_user
    )
  
  def setUp(self):
    # https://docs.djangoproject.com/en/5.2/topics/testing/tools/#the-test-client
    self.client = Client()

  def test_reject_disallowed_method(self):
    """Allowed methods are tested separately."""
    
    client: Client = self.client
    target_url: str = f"/api/tag/{self.test_tag.id}"
    
    expected_message: bytes = \
      b"This resource requires GET, PUT or DELETE method."
    post_request_data: dict = {
      "user-id": f"{self.test_user.id}",
      "tag-name": "new_test_tag_name"
    }
    response = client.post(target_url, post_request_data)
    self.assertEqual(response.status_code, 405)
    self.assertEqual(response.content, expected_message)
    response = client.patch(target_url)
    self.assertEqual(response.status_code, 405)
    self.assertEqual(response.content, expected_message)

  def test_user_auth(self):
    ...
  
  def test_user_ownership(self):
    ...
  
  def test_reject_malformed_request(self):
    client: Client = self.client
    
    # Case 1: improper PUT data
    target_url: str = f"/api/tag/{self.test_tag.id}"
    put_request_data: dict = {
      "some-data": "random",
      "matches-requirements": "false"
    }
    response = client.put(target_url, json.dumps(put_request_data))
    self.assertEqual(response.status_code, 400)

    # Case 2: request on non-existent tag
    # use a random valid UUID to match URL pattern
    target_url: str = "/api/tag/31b4354d-9dcb-40bc-8230-8b83bd8ff863"
    response = client.delete(target_url)
    self.assertEqual(response.status_code, 400)
    # using valid PUT data
    put_request_data: dict = {
      "user-id": f"{self.test_user.id}",
      "tag-name": "new_test_tag_name"
    }
    response = client.put(target_url, json.dumps(put_request_data))
    self.assertEqual(response.status_code, 400)
  
  def test_respond_to_GET_request(self):
    client: Client = self.client
    target_url: str = f"/api/tag/{self.test_tag.id}"
    
    response = client.get(target_url)
    expected_data: dict = {
      'tag-id': f"{self.test_tag.id}",
      'tag-name': f"{self.test_tag.name}",
      'tag-owner': f"{self.test_user.id}"
    }
    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), expected_data)

  def test_respond_to_DELETE_request(self):
    client: Client = self.client
    target_url: str = f"/api/tag/{self.test_tag.id}"

    expected_data = { "tag-id": f"{self.test_tag.id}" }
    response = client.delete(target_url)
    response_data = json.loads(response.content)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response_data, expected_data)
    # tag actually deleted
    with self.assertRaises(Tag.DoesNotExist):
      Tag.objects.get(id=self.test_tag.id)  # error expected
  
  def test_respond_to_PUT_request(self):
    client: Client = self.client
    target_url: str = f"/api/tag/{self.test_tag.id}"

    put_request_data: dict = {
      "user-id": f"{self.test_user.id}",
      "tag-name": "new_test_tag_name"
    }
    expected_data: dict = {
      "tag-id": f"{self.test_tag.id}",
      "tag-name": "new_test_tag_name"
    }
    response = client.put(target_url, json.dumps(put_request_data))
    response_data = json.loads(response.content)
    updated_tag: Tag = Tag.objects.get(id=self.test_tag.id)
    self.assertEqual(response.status_code, 200)
    # test object actually updated in backend
    self.assertEqual(response_data, expected_data)
    self.assertEqual(response_data['tag-name'], updated_tag.name)


class NewTagViewTestCase(TestCase):
  """Tests the new_tag_view, including GET and POST methods.
  GET: return required details for creating a new Tag object.
  POST: create a new Tag object with given tag-name and owner by user-id.
  """

  @classmethod
  def setUpTestData(cls) -> None:
    cls.test_user: AppUser = AppUser.objects.create(username="test_user_1")
  
  def setUp(self):
    # https://docs.djangoproject.com/en/5.2/topics/testing/tools/#the-test-client
    self.client = Client()
  
  def test_reject_disallowed_methods(self):
    """Allowed methods are tested separately."""

    client: Client = self.client
    target_url: str = "/api/tag/new"
    
    expected_message: bytes = \
      b"This resource requires GET or POST method."
    response = client.delete(target_url)
    self.assertEqual(response.status_code, 405)
    self.assertEqual(response.content, expected_message)
    response = client.patch(target_url)
    self.assertEqual(response.status_code, 405)
    self.assertEqual(response.content, expected_message)
  
  def test_user_auth(self):
    ...
  
  def test_reject_malformed_request(self):
    client: Client = self.client
    
    target_url: str = "/api/tag/new"
    post_request_data: dict = {
      "some-data": "random",
      "matches-requirements": "false"
    }
    response = client.post(target_url, post_request_data)
    self.assertEqual(response.status_code, 400)
  
  def test_respond_to_GET_request(self):
    client: Client = self.client
    target_url: str = "/api/tag/new"
    
    response = client.get(target_url)
    expected_data: bytes = \
      b"Requires POST request with data:" \
      b"{" \
      b"  user-id: uuid of resource owner," \
      b"  tag-name: string name to give specified tag " \
      b"}"
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, expected_data)
  
  def test_respond_to_POST_request(self):
    client: Client = self.client
    target_url: str = "/api/tag/new"

    post_request_data: dict = {
      "user-id": f"{self.test_user.id}",
      "tag-name": "new_test_tag_name"
    }
    expected_name: str = "new_test_tag_name"
    response = client.post(target_url, post_request_data)
    response_data = json.loads(response.content)
    new_tag: Tag = Tag.objects.get()  # the only Tag is the one we just made
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response_data['tag-name'], expected_name)
    self.assertEqual(response_data['tag-id'], str(new_tag.id))
    # test object actually created in backend, with correct name
    self.assertEqual(new_tag.name, expected_name)


class ExistingImageTagViewTestCase(TestCase):
  """Tests the existing_imagetag_view, including GET and DELETE methods.
  GET: return details of the ImageTag object noted by request.imagetag_id.
  DELETE: delete the ImageTag object noted by request.imagetag_id.
  """

  @classmethod
  def setUpTestData(cls) -> None:
    cls.test_user: AppUser = AppUser.objects.create(username="test_user_1")
    cls.test_image: Image = Image.objects.create(
      source="test.png",
      owner=cls.test_user,
      description="this is the test image description"
    )
    cls.test_tag: Tag = Tag.objects.create(
      name="test_tag",
      owner=cls.test_user
    )
    cls.test_imagetag: ImageTag = ImageTag.objects.create(
      image_id=cls.test_image,
      tag_id=cls.test_tag
    )
  
  def setUp(self):
    # https://docs.djangoproject.com/en/5.2/topics/testing/tools/#the-test-client
    self.client = Client()

  def test_reject_disallowed_method(self):
    """Allowed methods are tested separately."""

    client: Client = self.client
    target_url: str = f"/api/image-tag/{self.test_imagetag.id}"
    
    expected_message: bytes = \
      b"This resource requires GET or DELETE method."
    put_request_data: dict = {
      "user-id": f"{self.test_user.id}",
      "tag-id": "31b4354d-9dcb-40bc-8230-8b83bd8ff863"
    }
    response = client.put(target_url, json.dumps(put_request_data))
    self.assertEqual(response.status_code, 405)
    self.assertEqual(response.content, expected_message)
    response = client.patch(target_url)
    self.assertEqual(response.status_code, 405)
    self.assertEqual(response.content, expected_message)
  
  def test_user_auth(self):
    ...
  
  def test_user_ownership(self):
    ...

  def test_respond_to_GET_request(self):
    client: Client = self.client
    target_url: str = f"/api/image-tag/{self.test_imagetag.id}"
    
    response = client.get(target_url)
    expected_data: dict = {
      "imagetag-id": f"{self.test_imagetag.id}",
      "image-id": f"{self.test_imagetag.image_id}",
      "tag-id": f"{self.test_imagetag.tag_id}"
    }
    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), expected_data)

  def test_respond_to_DELETE_request(self):
    client: Client = self.client
    target_url: str = f"/api/image-tag/{self.test_imagetag.id}"

    expected_data = { "imagetag-id": f"{self.test_imagetag.id}" }
    response = client.delete(target_url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), expected_data)
    # ImageTag actually deleted
    with self.assertRaises(ImageTag.DoesNotExist):
      ImageTag.objects.get(id=self.test_imagetag.id)  # error expected


class NewImageTagViewTestCase(TestCase):
  """Tests the new_imagetag_view, including GET and POST methods.

  GET: return required details for creating a new ImageTag object.
  POST: create a new ImageTag object associating image-id with tag-id.
  """

  @classmethod
  def setUpTestData(cls) -> None:
    cls.test_user: AppUser = AppUser.objects.create(username="test_user_1")
    cls.test_image: Image = Image.objects.create(
      source="test.png",
      owner=cls.test_user,
      description="this is the test image description"
    )
    cls.test_tag: Tag = Tag.objects.create(
      name="test_tag",
      owner=cls.test_user
    )
    cls.test_user_2: AppUser = AppUser.objects.create(username="other_user")
  
  def setUp(self):
    # https://docs.djangoproject.com/en/5.2/topics/testing/tools/#the-test-client
    self.client = Client()

  def test_reject_disallowed_method(self):
    """Allowed methods are tested separately."""

    client: Client = self.client
    target_url: str = "/api/image-tag/new"
    
    expected_message: bytes = \
      b"This resource requires GET or POST method."
    response = client.delete(target_url)
    self.assertEqual(response.status_code, 405)
    self.assertEqual(response.content, expected_message)
    response = client.patch(target_url)
    self.assertEqual(response.status_code, 405)
    self.assertEqual(response.content, expected_message)

  def test_user_auth(self):
    ...

  def test_user_ownership(self):
    client: Client = self.client
    target_url: str = "/api/image-tag/new"

    post_request_data: dict = {
      "user-id": f"{self.test_user_2.id}",  # non-owner user
      "tag-id": f"{self.test_tag.id}",
      "image-id": f"{self.test_image.id}"
    }
    response = client.post(target_url, post_request_data)
    self.assertEqual(response.status_code, 403)

  def test_reject_malformed_request(self):
    client: Client = self.client
    
    target_url: str = "/api/image-tag/new"
    post_request_data: dict = {
      "some-data": "random",
      "matches-requirements": "false"
    }
    response = client.post(target_url, post_request_data)
    self.assertEqual(response.status_code, 400)

  def test_respond_to_GET_request(self):
    client: Client = self.client
    target_url: str = "/api/image-tag/new"
    
    response = client.get(target_url)
    expected_data: bytes = \
      b"Requires POST request with data:" \
      b"{" \
      b"  user-id: uuid of resource owner," \
      b"  image-id: uuid of image to apply tag," \
      b"  tag-id: uuid of tag to apply to image " \
      b"}"
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, expected_data)

  def test_respond_to_POST_request(self):
    client: Client = self.client
    target_url: str = "/api/image-tag/new"

    post_request_data: dict = {
      "user-id": f"{self.test_user.id}",
      "tag-id": f"{self.test_tag.id}",
      "image-id": f"{self.test_image.id}"
    }
    response = client.post(target_url, post_request_data)
    response_data = json.loads(response.content)
    # The only ImageTag is the one we just made
    new_imagetag: ImageTag = ImageTag.objects.get()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response_data['imagetag-id'], str(new_imagetag.id))
    # check object actually created in backend
    self.assertEqual(new_imagetag.image_id.id, self.test_image.id)
    self.assertEqual(new_imagetag.tag_id.id, self.test_tag.id)
