from django import forms
from django.contrib.auth.models import User
from grumblr.models import *

class RegistrationForm(forms.Form):
    #add styling to form: https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
    firstname = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=200, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match.")
        return cleaned_data
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact='username'):
            raise forms.ValidationError("Username is already taken")
        return username

class AdditionalInfoForm(forms.ModelForm):
    age = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    short_bio = forms.CharField(max_length=420, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField()

    class Meta:
        model = UserInfo
        fields = ('age', 'short_bio', 'profile_picture',)
        widget = {'picture':forms.FileInput()}