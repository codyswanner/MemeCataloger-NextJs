from django.test import TestCase
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
    test_tag: Tag = Tag.objects.get(username="test_user_1")
    self.assertIsNotNone(test_tag)

  def test_tag_id_is_uuid(self) -> None:
    test_tag: Tag = Tag.objects.get(source="test_source.png")
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
class UrlsTestCase(TestCase):
  def setUp(self) -> None:
    ...
  
  """
    So here's what I'm thinking for this one:
    Need a test client (for details see: https://docs.djangoproject.com/en/5.2/topics/testing/tools/#the-test-client)
    that will navigate to each api URL and validate that it is returning the
    expected data... but to make that work, there needs to be data.
    Manually creating data for each URL is annoying and hard to read,
    so look into using fixtures: https://docs.djangoproject.com/en/5.2/topics/testing/tools/#fixture-loading

    That should be a sane way to do this testing without too much fuss.
  """


"""Tests for views.py"""



