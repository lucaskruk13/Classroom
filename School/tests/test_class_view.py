from django.test import TestCase
import random
from django.shortcuts import reverse
from django.contrib.auth.models import User
from School.models import Class, School
from Account.models import Profile

# Create your tests here.
class ClassTest(TestCase):

    @classmethod
    def setUpClass(cls):

        # unauthenticated URL
        cls.class_url = reverse("class", kwargs={"pk":1})
        super(ClassTest, cls).setUpClass()  # Have the superclass setup

    def setUp(self):
        self.unauthenticated_response = self.client.get(self.class_url)

        # Authenticate
        self.client.login(username=self.username, password=self.password)

        self.authenticated_response = self.client.get(self.class_url)

        super().setUp()

    @classmethod
    def setUpTestData(cls):
        cls.school = School.objects.create(name='Pisgah', location='Canton, NC', mascot='Bears')

        # Create the First Teacher
        cls.username = 'johnappleseed'
        cls.password = 'secret123'

        cls.user = User.objects.create(first_name='John', last_name='Appleseed', email='john@appleseed.com',username=cls.username)
        cls.user.set_password(cls.password)

        cls.user.profile.status = 'TR' # Set it to a Teacher
        cls.user.save()

        # Create A School
        school = School.objects.create(name='Pisgah', location='Canton, NC', mascot='Black Bears')

        # Create a Class
        pe = Class.objects.create(name='PE', subject='Physical Education', start_time='12:00:00', school=school)

        # Add the Teacher Profile
        pe.profiles.add(cls.user.profile)
        pe.save()

        for i in range(20):

            # Create a new Students
            student = User.objects.create(username="Student{}".format(str(i+1)), first_name="Student", last_name="{}".format(str(i+1)))
            student.profile.status='SR'
            student.save()

            # Save the Class
            pe.profiles.add(student.profile)
            pe.save()

    def test_redirects_to_login_when_not_logged_in(self):
        self.assertRedirects(self.unauthenticated_response, '/login/?next=/class/1/')

    def test_can_get_class_page_when_logged_in(self):
        self.assertEqual(self.authenticated_response.status_code, 200)

    def test_there_are_twenty_students_and_a_teacher_to_each_class(self):
        this_class = Class.objects.get(name='PE')
        self.assertEqual(this_class.profiles.count(), 21)

        # Test there are 20 students, who are Seniors
        self.assertEqual(this_class.profiles.filter(status='SR').count(), 20)

        # Test There are no Freshman
        self.assertEqual(this_class.profiles.filter(status='FR').count(), 0)

        # Test there is one Teacher
        self.assertEqual(this_class.profiles.filter(status='TR').count(), 1)

