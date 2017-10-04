# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse, get_object_or_404
from grumblr.models import *
from grumblr.forms import *

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
        context['form'] = RegistrationForm()
        return render(request, 'grumblr/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/register.html', context)

    new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'],
                                        first_name=request.POST['first_name'], last_name=request.POST['last_name'], is_active=False)
    new_user.save()

    token = default_token_generator.make_token(new_user)
    email_body = """
    Please click the link below to verify your email address and complete the registration of your account:
    
    http://%s%s 
    """ % (request.get_host(),
           reverse('confirm_registration', args=(new_user.username, token)))

    send_mail(subject="Verify your email address", message=email_body, from_email="nfajriya@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']

    return render(request, 'grumblr/need_confirmation.html', context)

def confirm_registration(request, username, token):
    context = {}
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()
    context['is_new'] = 'True'
    return render(request, 'grumblr/loginpage.html', context)

def loginsuccess(request):
    try:
        UserInfo.objects.get(user_id=request.user)
    except ObjectDoesNotExist:
        return redirect('/additionalinfo')
    return redirect('/globalstream')

@login_required
def additionalinfo(request):
    context = {}

    if request.method == 'GET':
        context['form'] = AdditionalInfoForm()
        return render(request, 'grumblr/additionalinfo.html', context)

    new_info = UserInfo(user_id=request.user)
    form = AdditionalInfoForm(request.POST, request.FILES, instance=new_info)
    if not form.is_valid:
        context['form'] = form
        return render(request, 'grumblr/additionalinfo.html', context)
    form.save()
    return redirect('/globalstream')

def nofoundpage(request):
    return render(request, 'grumblr/404.html')