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


"""Tests for models.py"""
from .models import *
from django.db.utils import IntegrityError

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

class UrlUserTestCase(TestCase):
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


class UrlImageTestCase(TestCase):
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


class UrlTagTestCase(TestCase):
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


class UrlImageTagTestCase(TestCase):
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
