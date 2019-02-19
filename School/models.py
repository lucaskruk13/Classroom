from django.db import models
from Account.models import Profile
from django.utils.timezone import now
from datetime import datetime as dt

class School(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    location = models.CharField(max_length=100, blank=False, null=False)
    mascot = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return "{} | {}".format(self.name, self.location)

class Class(models.Model):

    school = models.ForeignKey(School, related_name='school_class', on_delete=models.CASCADE)
    profiles = models.ManyToManyField(Profile)
    name = models.CharField(max_length=100, blank=False, null=False)
    subject = models.CharField(max_length=20, blank=False, null=False)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, default=now)

    def __str__(self):
        return "{}: {}".format(self.start_time, self.name)

class Session(models.Model):
    associated_class = models.ForeignKey(Class, related_name='class_session', on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False, default=now)
    absences = models.ManyToManyField(Profile, blank=True)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{}, {}".format(self.date, self.summary)
