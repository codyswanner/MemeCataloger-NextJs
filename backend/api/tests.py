"""Django tests for the api module.
Includes tests for the models and for the URLs/Views (together).
Intentionally excludes the following modules:
 - __init__: who tests init?  Is that a thing people do?
 - admin: not currently in use.
 - apps: Django boilerplate code
 - serializers: restframework boilerplace code
"""

from django.test import Client, TestCase
import re
import json
from .models import AppUser, Image, Tag, ImageTag
from django.db.utils import IntegrityError
from django.conf import settings
from unittest.mock import Mock
from pathlib import Path


"""Tests for models.py"""

class AppUserTestCase(TestCase):
  def setUp(self) -> None:
    AppUser.objects.create(username="test_user_1")
  
  def test_user_exists(self) -> None:
    test_user: AppUser = AppUser.objects.get(username="test_user_1")
    self.assertIsNotNone(test_user)
  
  def test_user_id_is_uuid(self) -> None:
    test_user: AppUser = AppUser.objects.get(username="test_user_1")
    self.assertNotEqual(test_user.id, 1)  # non-uuid default is 1
    is_uuid = re.fullmatch(
      r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$',
      str(test_user.id)
    )
    self.assertTrue(is_uuid)

  def test_usernames_must_be_unique(self) -> None:
    try:
      test_user_1: AppUser = AppUser(username="test1")
      test_user_1.save()
      # Attempt to use same username again; error expected
      test_user_2: AppUser = AppUser(username="test1")
      test_user_2.save()
      # error expected; if we arrive here, fail the test
      self.fail("Allowed same username twice; fail")
    except IntegrityError:
      pass # error is correct behavior


class ImageTestCase(TestCase):
  def setUp(self) -> None:
    test_user: AppUser = AppUser.objects.create(username="test_user_1")
    Image.objects.create(source="test_source.png", owner=test_user)

  def test_image_exists(self) -> None:
    test_image: Image = Image.objects.get(source="test_source.png")
    self.assertIsNotNone(test_image)

  def test_image_id_is_uuid(self) -> None:
    test_image: Image = Image.objects.get(source="test_source.png")
    self.assertNotEqual(test_image.id, 1)  # non-uuid default is 1
    is_uuid = re.fullmatch(
      r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$',
      str(test_image.id)
    )
    self.assertTrue(is_uuid)

  def test_image_takes_description(self) -> None:
    test_image: Image = Image.objects.get(source="test_source.png")
    description_string: str = "This is a test description"
    test_image.description = description_string
    test_image.save()
    self.assertEqual(test_image.description, description_string)


class TagTestCase(TestCase):
  def setUp(self) -> None:
    test_user: AppUser = AppUser.objects.create(username="test_user_1")
    Tag.objects.create(name="test_tag", owner=test_user)

  def test_tag_exists(self) -> None:
    test_tag: Tag = Tag.objects.get(name="test_tag")
    self.assertIsNotNone(test_tag)

  def test_tag_id_is_uuid(self) -> None:
    test_tag: Tag = Tag.objects.get(name="test_tag")
    self.assertNotEqual(test_tag.id, 1)  # non-uuid default is 1
    is_uuid = re.fullmatch(
      r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$',
      str(test_tag.id)
    )
    self.assertTrue(is_uuid)


class ImageTagTestCase(TestCase):
  def setUp(self) -> None:
    test_user: AppUser = AppUser.objects.create(username="test_user_1")
    test_image: Image = Image.objects.create(
      source="test.png",
      owner=test_user
    )
    test_tag: Tag = Tag.objects.create(name="test_tag", owner=test_user)
    ImageTag.objects.create(image_id=test_image, tag_id=test_tag)

  def test_imagetag_exists(self) -> None:
    test_image: Image = Image.objects.get(source="test.png")
    test_tag: Tag = Tag.objects.get(name="test_tag")
    test_imagetag: ImageTag = ImageTag.objects.get(
      image_id=test_image,
      tag_id=test_tag
    )
    self.assertIsNotNone(test_imagetag)


"""Tests for urls.py"""

class UrlUserListTestCase(TestCase):
  """Simultaneously tests the URL and View for retrieving user data.
  (Simultaneous because they are heads and tails of the same coin,
  and I am too lazy to be strict about "unit" testing.)
  """
  @classmethod
  def setUpTestData(cls):
    cls.test_user: AppUser = AppUser.objects.create(username="test_user_1")
  
  def setUp(self):
    # https://docs.djangoproject.com/en/5.2/topics/testing/tools/#the-test-client
    self.client = Client()
    self.response = self.client.get('/api/user/')
  
  def test_successful_response(self):
    # "If it can fail here, it can fail anywhere"
    # -- famous New York quote, paraphrased
    self.assertEqual(self.response.status_code, 200)
  
  def test_user_data_is_as_expected(self):
    # There is only one user in the test database; grab their data
    test_user_data = self.response.json()[0]
    self.assertEqual(test_user_data["username"], 'test_user_1')
    # And also check ID? -\(?)/-
  
  def test_no_unexpected_data(self):
    # Know how I said earlier that there's only one user?
    # Well, if there's more than one, we have a problem.
    with self.assertRaises(IndexError):
      self.response.json()[1]


class UrlImageListTestCase(TestCase):
  """Simultaneously tests the URL and View for retrieving image data.
  (Simultaneous because they are heads and tails of the same coin,
  and I am too lazy to be strict about "unit" testing.)
  """
  @classmethod
  def setUpTestData(cls) -> None:
    cls.test_user: AppUser = AppUser.objects.create(username="test_user_1")
    cls.test_image: Image = Image.objects.create(
      source="test.png",
      owner=cls.test_user,
      description="this is the test image description"
    )
  
  def setUp(self):
    # https://docs.djangoproject.com/en/5.2/topics/testing/tools/#the-test-client
    self.client = Client()
    self.response = self.client.get('/api/image/')
  
  def test_successful_response(self):
    # "If it can fail here, it can fail anywhere"
    # -- famous New York quote, paraphrased
    self.assertEqual(self.response.status_code, 200)
  
  def test_image_data_is_as_expected(self):
    # There is only one image in the test database; grab it's data
    test_image_data = self.response.json()[0]
    self.assertEqual(
      test_image_data["source"],
      'http://testserver/media/test.png')
    self.assertEqual(
      test_image_data['owner'],
      str(self.test_user.id)
    )
    self.assertEqual(
      test_image_data["description"],
      "this is the test image description"
    )
    # And also check ID? -\(?)/-
  
  def test_no_unexpected_data(self):
    # Know how I said earlier that there's only one image?
    # Well, if there's more than one, we have a problem.
    with self.assertRaises(IndexError):
      self.response.json()[1]


class UrlTagListTestCase(TestCase):
  """Simultaneously tests the URL and View for retrieving tag data.
  (Simultaneous because they are heads and tails of the same coin,
  and I am too lazy to be strict about "unit" testing.)
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
    self.response = self.client.get('/api/tag/')
  
  def test_successful_response(self):
    # "If it can fail here, it can fail anywhere"
    # -- famous New York quote, paraphrased
    self.assertEqual(self.response.status_code, 200)

  def test_image_data_is_as_expected(self):
    # There is only one tag in the test database; grab it's data
    test_tag_data = self.response.json()[0]
    self.assertEqual(
      test_tag_data["name"],
      'test_tag')
    self.assertEqual(
      test_tag_data['owner'],
      str(self.test_user.id)
    )
    # And also check ID? -\(?)/-
  
  def test_no_unexpected_data(self):
    # Know how I said earlier that there's only one image?
    # Well, if there's more than one, we have a problem.
    with self.assertRaises(IndexError):
      self.response.json()[1]


class UrlImageTagListTestCase(TestCase):
  """Simultaneously tests the URL and View for retrieving imagetag data.
  (Simultaneous because they are heads and tails of the same coin,
  and I am too lazy to be strict about "unit" testing.)
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
    self.response = self.client.get('/api/image-tag/')
  
  def test_successful_response(self):
    # "If it can fail here, it can fail anywhere"
    # -- famous New York quote, paraphrased
    self.assertEqual(self.response.status_code, 200)

  def test_image_data_is_as_expected(self):
    # There is only one imagetag in the test database; grab it's data
    test_imagetag_data = self.response.json()[0]
    self.assertEqual(
      test_imagetag_data["image_id"],
      str(self.test_image.id))
    self.assertEqual(
      test_imagetag_data['tag_id'],
      str(self.test_tag.id)
    )
    # And also check ID? -\(?)/-
  
  def test_no_unexpected_data(self):
    # Know how I said earlier that there's only one image?
    # Well, if there's more than one, we have a problem.
    with self.assertRaises(IndexError):
      self.response.json()[1]


class UrlUserTestCase(TestCase):
  """Basic test for the (not fully implemented) /user/[id] path.
  Really we're just looking for it to return 200 and have the expected data."""
  @classmethod
  def setUpTestData(cls):
    cls.test_user: AppUser = AppUser.objects.create(username="test_user_1")
  
  def setUp(self):
    # https://docs.djangoproject.com/en/5.2/topics/testing/tools/#the-test-client
    self.client = Client()
    self.response = self.client.get(f'/api/user/{self.test_user.id}')
  
  def test_successful_response(self):
    # "If it can fail here, it can fail anywhere"
    # -- famous New York quote, paraphrased
    self.assertEqual(self.response.status_code, 200)
  
  def test_expected_content(self):
    """Docstring here to explain the expected_content variable.
    The expected response of this page is a bytestring containing basic HTML.
    This HTML will include the UUID of the test_user, i.e. self.test_user.id
    The expected_content variable is built by starting with some normal strings
    that include the HTML we expect, and also a format string that allows
    inserting the dynamic self.test_user.id value into the string.
    These strings are concatenated together and then encoded to a bytestring
    with UTF-8.

    It's a little complex, but it does match expected output of this page,
    and with this very long comment may make some more sense.
    
    Added bit of context; curly braces in f-strings are escaped by using
    double-curly braces, hence those in this string.
    Author advises against touching any braces, parentheses or quotes here.
    """

    expected_content: bytes = "<div>You landed on the user view!</div>" \
    "<div>The user id is: " \
    f"{{'user_id': UUID('{self.test_user.id}')}}</div>" \
    "<div>This page hasn't really been implemented for anything yet.</div>" \
    .encode('UTF-8')
    self.assertEqual(self.response.content, expected_content)
  

class UrlImageTestCase(TestCase):
  """Tests for the /image/[id] path.
  Expected to simply show the image with given id."""

  @classmethod
  def setUpTestData(cls):
    # Create a user to own the image
    cls.test_user: AppUser = AppUser.objects.create(username="test_user_1")
    # Create the file for the image record to point to
    # This will be the response.content of the URL
    cls.mock_file: Mock = Mock()
    cls.mock_file.name = "test_file.webp"
    cls.mock_file.src = (
      b"52494646be000000574542505650384c0d0a0055000000c4401e32"
      b"0500000070bf17f57c9f0412003c078000100c28064000a24b0e52"
      b"a0002000000004600"
    )
    # Store the file so it can be accessed
    app_media_root: str = settings.MEDIA_ROOT
    file = open(f"{app_media_root}/{cls.mock_file.name}", "w+b")
    file.write(cls.mock_file.src)
    file.close()
    # Create the image record in the database; includes the image id
    cls.test_image: Image = Image.objects.create(
      source=f"{cls.mock_file.name}",
      owner=cls.test_user
    )
  
  @classmethod
  def tearDownClass(cls) -> None:
    # Delete the test image file at the end of testing
    test_file = Path(f"{settings.MEDIA_ROOT}/{cls.mock_file.name}")
    test_file.unlink(missing_ok=True)
    # And maintain all the normal teardowns
    return super().tearDownClass()

  def setUp(self):
    # https://docs.djangoproject.com/en/5.2/topics/testing/tools/#the-test-client
    self.client = Client()
    self.response = self.client.get(f'/api/image/{self.test_image.id}')

  def test_successful_response(self):
    # "If it can fail here, it can fail anywhere"
    # -- famous New York quote, paraphrased
    self.assertEqual(self.response.status_code, 200)

  def test_expected_content(self):
    # this is the bytestring representing the image;
    # see the setUpTestData function
    expected_data: bytes = b'52494646be000000574542505' \
    b'650384c0d0a0055000000c4401e320500000070bf17f57c9f041' \
    b'2003c078000100c28064000a24b0e52a0002000000004600'
    # content of the page should simply be the test image
    self.assertEqual(expected_data, self.response.content)


"""Tests for views.py"""

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
  
  def test_respond_to_PUT_request(self):
    client: Client = self.client
    target_url: str = f"/api/tag/{self.test_tag.id}"

    put_request_data: dict = {
      "user-id": f"{self.test_user.id}",
      "tag-name": "new_test_tag_name"
    }
    response = client.put(target_url, json.dumps(put_request_data))
    self.assertEqual(response.status_code, 200)
    # successful response echos back the data that was sent
    self.assertEqual(json.loads(response.content), put_request_data)


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
      b"  tag-name: string name to give specified tag" \
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
    uuid_regex: str = \
      r'[0-9a-fA-F]{8}\-' \
      r'[0-9a-fA-F]{4}\-' \
      r'[0-9a-fA-F]{4}\-' \
      r'[0-9a-fA-F]{4}\-' \
      r'[0-9a-fA-F]{12}'
    expected_name: str = "new_test_tag_name"
    response = client.post(target_url, post_request_data)
    response_data = json.loads(response.content)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response_data['tag-name'], expected_name)
    self.assertRegex(response_data['tag-id'], uuid_regex)


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
      "imagetag-image": f"{self.test_imagetag.image_id}",
      "imagetag-tag": f"{self.test_imagetag.tag_id}"
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
      b"  tag-id: uuid of tag to apply to image" \
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
    uuid_regex: str = \
      r'[0-9a-fA-F]{8}\-' \
      r'[0-9a-fA-F]{4}\-' \
      r'[0-9a-fA-F]{4}\-' \
      r'[0-9a-fA-F]{4}\-' \
      r'[0-9a-fA-F]{12}'
    response = client.post(target_url, post_request_data)
    response_data = json.loads(response.content)
    self.assertEqual(response.status_code, 200)
    self.assertRegex(response_data['imagetag-id'], uuid_regex)
