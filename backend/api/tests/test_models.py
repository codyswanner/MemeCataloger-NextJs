"""Tests for Django models in the api package.
Test classes in this module check their target model for:
  - successful creation of a test object
  - a valid UUID assigned to the test object
  - any custom fields on the model
"""

from django.test import TestCase
import re
from api.models import AppUser, Image, Tag, ImageTag
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
      r'^[0-9a-fA-F]{8}' \
      r'-[0-9a-fA-F]{4}' \
      r'-4[0-9a-fA-F]{3}' \
      r'-[89aAbB][0-9a-fA-F]{3}' \
      r'-[0-9a-fA-F]{12}$',
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
      r'^[0-9a-fA-F]{8}' \
      r'-[0-9a-fA-F]{4}' \
      r'-4[0-9a-fA-F]{3}' \
      r'-[89aAbB][0-9a-fA-F]{3}' \
      r'-[0-9a-fA-F]{12}$',
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
      r'^[0-9a-fA-F]{8}' \
      r'-[0-9a-fA-F]{4}' \
      r'-4[0-9a-fA-F]{3}' \
      r'-[89aAbB][0-9a-fA-F]{3}' \
      r'-[0-9a-fA-F]{12}$',
      str(test_tag.id)
    )
    self.assertTrue(is_uuid)


class ImageTagTestCase(TestCase):
  def setUp(self) -> None:
    self.test_user: AppUser = AppUser.objects.create(username="test_user_1")
    self.test_image: Image = Image.objects.create(
      source="test.png",
      owner=self.test_user
    )
    self.test_tag: Tag = Tag.objects.create(
      name="test_tag",
      owner=self.test_user
    )
    ImageTag.objects.create(image_id=self.test_image, tag_id=self.test_tag)

  def test_imagetag_exists(self) -> None:
    test_image: Image = Image.objects.get(source="test.png")
    test_tag: Tag = Tag.objects.get(name="test_tag")
    test_imagetag: ImageTag = ImageTag.objects.get(
      image_id=test_image,
      tag_id=test_tag
    )
    self.assertIsNotNone(test_imagetag)

  def test_imagetag_id_is_uuid(self) -> None:
    test_imagetag: ImageTag = ImageTag.objects.get(image_id=self.test_image)
    is_uuid = re.fullmatch(
      r'^[0-9a-fA-F]{8}' \
      r'-[0-9a-fA-F]{4}' \
      r'-4[0-9a-fA-F]{3}' \
      r'-[89aAbB][0-9a-fA-F]{3}' \
      r'-[0-9a-fA-F]{12}$',
      str(test_imagetag.id)
    )
    self.assertTrue(is_uuid)
