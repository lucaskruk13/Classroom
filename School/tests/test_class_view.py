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
        cls.unathenticated_url = reverse("class", kwargs={"pk":1})
        super(ClassTest, cls).setUpClass()  # Have the superclass setup

    @classmethod
    def setUpTestData(cls):
        cls.school = School.objects.create(name='Pisgah', location='Canton, NC', mascot='Bears')

        # Create 100 Students
        for i in range(400):
            c = User.objects.create(username=str(i), first_name=str(i), last_name=str(i))
            c.profile.status = 'FR'
            c.save()

        classes = [] # Empty list to store the classes so that we dont have to call the database over and over
        # Create 20 Classes
        for i in range(20):
           classes.append(Class.objects.create(school=cls.school))

        # Assign the students at random to each class. Each should be 20 in size
        for c in classes:
            for i in range(20):
                rand = random.randint(1,399)
                p = Profile.objects.get(pk=rand)
                c.profiles.add(p)
                c.save()


    def test_redirects_to_login_when_unauthenticated(self):
        unauthenticated_response = self.client.get(self.unathenticated_url)

        # Redirects to the login page with the previous page in next
        self.assertRedirects(unauthenticated_response, '/login/?next=/class/1/')
