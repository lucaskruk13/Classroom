from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from School.models import Class, School

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

    def test_redirect_to_login(self):
        # Since no user is authenticated, this needs to redriect to the login
        self.assertRedirects(self.feedResponse, '/login/?next=/')

    # With No Status, test it redirects

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

class AuthenticatedStudentTest(AuthenticatedFeedTest):
    def setUp(self):
        self.user.profile.status = 'SR'
        self.user.save()
        super().setUp()

    def test_is_student(self):
        self.assertEqual(self.user.profile.status, 'SR')

    def test_feed_is_student_view(self):

        self.assertContains(self.feedResponse, 'Student')

class AuthenticatedTeacherTest(AuthenticatedFeedTest):

    def setUp(self):
        self.user.profile.status = 'TR'
        self.user.save()
        super().setUp()

    def test_is_teacher(self):
        self.assertEqual(self.user.profile.status, 'TR')

    def test_feed_is_teacher_view(self):
        self.feedResponse = self.client.get(self.feed_url)
        self.assertContains(self.feedResponse, 'Teacher')

class TestFeedPageUserLoggedIn(AuthenticatedFeedTest):

    def setUp(self):
        super().setUp()


    def test_user_is_logged_in(self):
        self.assertTrue(self.user.is_authenticated)

class TestFeedClassesForTeacher(AuthenticatedTeacherTest):
    def setUp(self):

        self.school = School.objects.create(name='Pisgah', location='Canton, NC', mascot='Bears')
        self.class1 = Class.objects.create(school=self.school, name='Gym', subject='PE', start_time='06:00:00')
        self.class2 = Class.objects.create(school=self.school, name='Science', subject='Science', start_time='07:00:00')

        self.class1.profiles.add(self.user.profile)
        self.class2.profiles.add(self.user.profile)

        super().setUp()

    def test_feed_has_2_classes(self):
        self.assertContains(self.feedResponse, 'class-card', 2)

    def test_link_to_classes(self):

        self.assertContains(self.feedResponse, '<a href="%s">' % reverse('class',kwargs={"pk": self.class1.id}))
        self.assertContains(self.feedResponse, '<a href="%s">' % reverse('class', kwargs={"pk": self.class2.id}))


class TestFeedClassesForStudent(AuthenticatedStudentTest):
    def setUp(self):

        school = School.objects.create(name='Pisgah', location='Canton, NC', mascot='Bears')
        class1 = Class.objects.create(school=school, name='Gym', subject='PE', start_time='06:00:00')
        class2 = Class.objects.create(school=school, name='Science', subject='Science', start_time='07:00:00')

        class1.profiles.add(self.user.profile)
        class2.profiles.add(self.user.profile)

        super().setUp()

    def test_feed_has_2_classes(self):
        self.assertContains(self.feedResponse, 'class-card', 2)