# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
class UserInfo(models.Model):
    age = models.IntegerField(null=True)
    short_bio = models.TextField(max_length=420, null=True)
    profile_picture = models.ImageField(upload_to='static/grumblr/images', null=True)
    user_id = models.ForeignKey(User)

class BlogPost(models.Model):
    blog_text = models.TextField(max_length=42)
    published_time = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User)

    def __unicode__(self):
        return self.blog_text
