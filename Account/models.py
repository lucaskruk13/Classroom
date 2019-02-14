from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    STATUS = (
        ('FR','Freshman'),
        ('SO', 'Sophamore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('TR', 'Teacher'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS, null=True, blank=True)

    def __str__(self):
        return "{}, {}".format(self.user.last_name, self.user.first_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()