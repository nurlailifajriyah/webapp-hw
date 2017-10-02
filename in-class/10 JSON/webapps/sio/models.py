# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Student(models.Model):
    andrew_id = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    def __unicode__(self):
        return "%s %s (%s)" % (self.first_name, self.last_name,
                               self.andrew_id)
    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_entries(andrew_id):
        return Student.objects.filter(andrew_id=andrew_id).order_by('andrew_id')

class Course(models.Model):
    course_number = models.CharField(max_length=20, primary_key=True)
    course_name = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    students = models.ManyToManyField(Student)
    def __unicode__(self):
        return "%s: %s" % (self.course_number, self.course_name)
    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_entries():
        return Course.objects.all().order_by('course_number')
