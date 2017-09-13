from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Student(models.Model):
    andrewid = models.CharField(max_length=20)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    def __unicode__(self):
        return self.andrewid

class Course(models.Model):
    coursenumber = models.CharField(max_length=20)
    coursename = models.CharField(max_length=50)
    instructor = models.CharField(max_length=50)

    def __unicode__(self):
        return self.coursenumber