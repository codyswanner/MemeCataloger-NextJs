from django.test import Client, TestCase
from api.models import AppUser, Image, Tag, ImageTag
from django.conf import settings
from unittest.mock import Mock
from pathlib import Path


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

