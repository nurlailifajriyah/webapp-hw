from django import forms
from sio.models import *
from django.contrib.auth.models import User

class CreateStudentForm(forms.Form):
    andrewid = forms.CharField(max_length=20, primary_key=True)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    def clean_andrewid(self):
        # Confirms that the username is not already present in the
        # User model database.
        andrew_id = self.cleaned_data.get('andrewid')
        if Student.objects.filter(andrew_id=andrewid):
            raise forms.ValidationError("Andrew ID is already exist.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return andrewid

class CreateCourseForm(forms.Form):
    coursenumber = forms.CharField(max_length=20, primary_key=True)
    course_name = forms.CharField(max_length=255)
    instructor = forms.CharField(max_length=255)
    students = forms.ManyToManyField(Student)

    def clean_coursenumber(self):
        # Confirms that the username is not already present in the
        # User model database.
        course_number = self.cleaned_data.get('coursenumber')
        if Student.objects.filter(course_number=coursenumber):
            raise forms.ValidationError("Andrew ID is already exist.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return coursenumber

