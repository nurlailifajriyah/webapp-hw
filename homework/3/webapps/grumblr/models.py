# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class BlogPost(models.Model):
    blog_text = models.TextField()
    published_time = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User)

    def __unicode__(self):
        return self.blog_text
