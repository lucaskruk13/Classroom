from django.test import TestCase
from django.urls import reverse, resolve
from Account.views import signup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Account.models import Profile

# Create your tests here.
class SignUpTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SignUpTest, cls).setUpClass()  # Have the superclass setup

        # Class Level URLs
        cls.signup_url = reverse('signup')
        cls.feed_url = reverse('feed')

        # Class Level Views
        cls.signupView = resolve('/signup/')

        cls.signupData = {
            'username': 'john',
            'email': 'john@appleseed.com',
            'first_name': 'john',
            'last_name': 'appleseed',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',

        }

    def setUp(self):
        self.signupResponse = self.client.get(self.signup_url)
        self.signupPost = self.client.post(self.signup_url, self.signupData)

        self.feedResponse = self.client.get(self.feed_url)

class SignupPageSuccessfulTests(SignUpTest):

    def test_status_code(self):
        self.assertEquals(self.signupResponse.status_code, 200)

    def test_signup_resolves_signup_view(self):
        self.assertEquals(self.signupView.func, signup)

    def test_csrf(self):
        self.assertContains(self.signupResponse, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.signupResponse.context.get('form')
        self.assertIsInstance(form, UserCreationForm)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())


    def test_user_authentication(self):
        user = self.feedResponse.context.get('user')
        self.assertTrue(user.is_authenticated)


class SignupPageInvalidSubmission(SignUpTest):


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.signupData = {
            'username': 'john',
            'email': 'john@appleseed..com',
            'first_name': 'john',
            'last_name': 'appleseed',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',

        }

    def test_signup_status_code(self):
        self.assertEquals(self.signupPost.status_code, 200)

    def test_form_errors(self):
        form = self.signupPost.context.get('form')
        self.assertTrue(form.errors)

    def test_user_not_created(self):
        self.assertFalse(User.objects.exists())