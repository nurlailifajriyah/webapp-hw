# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
class RegToken(models.Model):
    user_id = models.ForeignKey(User)
    token = models.TextField()

class UserInfo(models.Model):
    age = models.IntegerField(null=True)
    short_bio = models.TextField(max_length=420, null=True)
    profile_picture = models.ImageField(upload_to='grumblr/images/profile_picture', null=True)
    user_id = models.OneToOneField(User, related_name='userinfo')

class Following(models.Model):
    user = models.ForeignKey(User, related_name='profile', default='')
    follow = models.ForeignKey(User, related_name='follow', default='')

    class Meta:
        unique_together = (("user", "follow"),)

class BlogPost(models.Model):
    blog_text = models.TextField(max_length=42)
    published_time = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.blog_text
