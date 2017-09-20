from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from smartfields import fields
from django.utils import timezone


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=140, default='')
    bio = models.TextField(blank=True, default='')
    avatar = fields.ImageField(upload_to='avatars/', blank=True, null=True)

    def get_short_name(self):
        return self.name.split(' ')[0]

    def get_full_name(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name',)


class Skills(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skills = models.CharField(max_length=15, default='')

    def __str__(self):
        return self.skills


#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_user_profile(sender, instance, created, **kwargs):
 #   if created:
 #       Profile.objects.create(user=instance)


#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()

def create_user_profile(sender, **kwargs):
    user = kwargs['instance']

    if kwargs['created']:
        Profile.objects.create(user=user)
post_save.connect(create_user_profile, sender=User)