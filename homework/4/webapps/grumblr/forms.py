from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    #add styling to form: https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
    firstname = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=200, label='Password', widget= forms.TextInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=200, label='Confirm Password', widget= forms.TextInput(attrs={'class': 'form-control'}))
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match.")
        return cleaned_datas
    def username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username_exact='username'):
            raise forms.ValidationError("Username is already taken")
        return username