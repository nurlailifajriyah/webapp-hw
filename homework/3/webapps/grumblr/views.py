# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from grumblr.models import *

# Create your views here.
def home(request):
    if request.user.is_authenticated():
        return redirect('/globalstream')
    else:
        return redirect('/login')

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect('/globalstream')
    items = BlogPost.objects.filter(user_id=user).order_by('-published_time')

    return render(request, 'grumblr/profile.html', {'items':items, 'user':user})
@login_required
def globalstream(request):
    items = BlogPost.objects.order_by('-published_time')

    return render(request, 'grumblr/globalstream.html', {'items':items})

@login_required
def add_item(request):
    errors = []  # A list to record messages for any errors we encounter.

    # Adds the new item to the database if the request parameter is present
    if not 'item' in request.POST or not request.POST['item']:
        errors.append('You must enter something.')
    else:
        new_item = BlogPost(blog_text=request.POST['item'], user_id=request.user)
        new_item.save()

    items = BlogPost.objects.order_by('-published_time')
    context = {'items':items, 'errors':errors}
    return render(request, 'grumblr/globalstream.html', context)

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

    if not 'firstname' in request.POST or not request.POST['username']:
        errors.append('First name is required.')
    else:
        context['firstname'] = request.POST['lastname']

    if not 'lastname' in request.POST or not request.POST['username']:
        errors.append('Last name is required.')
    else:
        context['lastname'] = request.POST['lastname']

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

    new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], \
                                        first_name=request.POST['firstname'], last_name=request.POST['lastname'])
    new_user.save()

    new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
    login(request, new_user)
    return redirect('/globalstream')

def nofoundpage(request):
    return render(request, 'grumblr/404.html')