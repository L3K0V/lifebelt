from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(max_length=16)
    github = models.CharField(max_length=48, blank=True)
    github_token = models.CharField(max_length=256, blank=True)
    avatar_url = models.URLField(blank=True)
