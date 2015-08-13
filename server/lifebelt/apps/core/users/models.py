from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    role = models.CharField(max_length=16)
    github = models.CharField(max_length=48, blank=True)
    github_token = models.CharField(max_length=256, blank=True)
    avatar_url = models.URLField(blank=True)

    @receiver(post_save, sender=User)
    def create_member_for_user(sender, instance=None, created=False, **kwargs):
        if created:
            Member.objects.get_or_create(user=instance)

    @receiver(pre_delete, sender=User)
    def delete_member_for_user(sender, instance=None, **kwargs):
        if instance:
            user_profile = Member.objects.get(user=instance)
            user_profile.delete()
