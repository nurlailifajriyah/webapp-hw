# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect
from grumblr.models import *

# Create your views here.
def register(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'grumblr/register.html', context)
    errors = []
    context['errors'] = errors

    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required')

    if 'password1' in request.POST and 'password2' in request.POST \
            and request.POST['password1'] and request.POST['password2'] \
            and request.POST['password1'] != request.POST['password2']:
        errors.append('Password did not match.')

    if len(User.objects.filter(username=request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if errors:
        return render(request, 'grumblr/register.html', context)

    new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
    new_user.save()

    new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
    login(request, new_user)
    return redirect('/login')
