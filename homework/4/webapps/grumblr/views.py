# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q
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
    context = {}
    context['page'] = "profile"
    #getting the loggedin user
    requester = request.user.username
    context['requester'] = requester
    #getting the user of the profile page
    try:
        user = User.objects.get(username=username)
        context['user'] = user
    except ObjectDoesNotExist:
        return redirect('/globalstream')
    #getting the user's blog posts
    items = BlogPost.objects.filter(user_id=user).order_by('-published_time')
    context['items'] = items
    #getting user info
    try:
        userinfo = UserInfo.objects.get(user_id=user)
    except ObjectDoesNotExist:
        return redirect('/globalstream')
    context['userinfo'] = userinfo
    follow = ''
    try:
        Following.objects.get(user=request.user, follow=user)
    except ObjectDoesNotExist:
        follow = 'Follow'
    except FieldDoesNotExist:
        follow = 'Follow'
    if follow == '':
        follow = 'Unfollow'

    context['follow'] = follow

    return render(request, 'grumblr/profile.html', context)
@login_required
def globalstream(request):
    context={}
    context['page'] = "globalstream"
    try:
        following = Following.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        context['items'] = BlogPost.objects.order_by('-published_time').filter(user_id=request.user)
        return render(request, 'grumblr/globalstream.html', context)
    #https://stackoverflow.com/questions/739776/django-filters-or
    context['items'] = BlogPost.objects.order_by('-published_time').filter(Q(user_id__in=following.values_list('follow', flat=True))| Q(user_id=request.user))
    try:
        context['userinfo'] = UserInfo.objects.all()
    except ObjectDoesNotExist:
        #todo
        return render(request, 'grumblr/404.html')
    return render(request, 'grumblr/globalstream.html', context)

@login_required
def add_item(request, page):
    errors = []  # A list to record messages for any errors we encounter.

    # Adds the new item to the database if the request parameter is present
    if not 'item' in request.POST or not request.POST['item']:
        errors.append('You must enter something.')
    else:
        new_item = BlogPost(blog_text=request.POST['item'], user_id=request.user)
        new_item.save()
    if page == 'profile':
        return redirect('/profile/'+request.user.username)
    else:
        return redirect('/globalstream')

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
    new_token = RegToken(user_id=new_user, token=token)
    new_token.save()

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

    recorded_token = RegToken.objects.get(user_id=user).token
    if recorded_token == token:
        user.is_active = True
        user.save()
        return render(request, 'grumblr/loginpage.html', context)
    return render(request, 'grumblr/404.html', context)

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

def follow(request, username):
    user = User.objects.get(username=username)
    following = Following(user=request.user, follow=user)
    following.save()
    return redirect('/profile/'+username)

def unfollow(request, username):
    user = User.objects.get(username=username)
    following = Following.objects.get(user=request.user, follow=user)
    following.delete()
    return redirect('/profile/'+username)

def editprofile(request, username):
    return redirect('/profile/' + username)