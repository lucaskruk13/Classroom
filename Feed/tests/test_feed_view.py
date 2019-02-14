from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
# Create your tests here.
class FeedTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(FeedTest, cls).setUpClass()  # Have the superclass setup

        # Class Level URLs
        cls.feed_url = reverse('feed')

    def setUp(self):

        self.feedResponse = self.client.get(self.feed_url)
        self.feedView = resolve('/')


class FeedViewTest(FeedTest):

    def test_can_get_feed(self):
        self.assertEqual(self.feedResponse.status_code, 200)


class AuthenticatedFeedTest(FeedTest):


    @classmethod
    def setUpClass(cls):
        super(AuthenticatedFeedTest, cls).setUpClass()

        # Create the First User
        cls.username = 'johnappleseed'
        cls.password = 'secret123'

        cls.user = User.objects.create(first_name='John', last_name='Appleseed', email='john@appleseed.com',
                                       username=cls.username)
        cls.user.set_password(cls.password)

        cls.user.save()

    def setUp(self):
        # Log the User In
        self.client.login(username=self.username, password=self.password)

        super().setUp()

class TestFeedPageUserLoggedIn(AuthenticatedFeedTest):

    def setUp(self):
        super().setUp()


    def test_user_is_logged_in(self):
        self.assertTrue(self.user.is_authenticated)
