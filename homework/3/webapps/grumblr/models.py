# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

# Data model for a todo-list item
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

class BlogPost(models.Model):
    blog_text = models.TextField()
    published_time = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User)


    def __unicode__(self):
        return self.blog_text
