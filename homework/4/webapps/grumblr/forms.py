from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput())
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match.")
        return cleaned_data
    def username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username_exact='username'):
            raise forms.ValidationError("Username is already taken")
