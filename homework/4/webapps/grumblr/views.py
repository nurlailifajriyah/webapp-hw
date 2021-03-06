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
    # getting the loggedin user
    requester = request.user.username
    context['requester'] = requester
    # getting the user of the profile page
    try:
        user = User.objects.get(username=username)
        context['user'] = user
    except ObjectDoesNotExist:
        return render(request, 'grumblr/404.html')
    # getting the user's blog posts
    items = BlogPost.objects.filter(user_id=user).order_by('-published_time')
    context['items'] = items
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
    # getting user info
    try:
        userinfo = UserInfo.objects.get(user_id=user)
    except ObjectDoesNotExist:
        return render(request, 'grumblr/profile.html', context)
    context['userinfo'] = userinfo


    return render(request, 'grumblr/profile.html', context)


@login_required
def globalstream(request):
    context = {}
    context['page'] = "globalstream"
    context['requester'] = request.user.username
    try:
        following = Following.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        context['items'] = BlogPost.objects.order_by('-published_time').filter(user_id=request.user)
        return render(request, 'grumblr/globalstream.html', context)
    # https://stackoverflow.com/questions/739776/django-filters-or
    context['items'] = BlogPost.objects.order_by('-published_time').filter(
        Q(user_id__in=following.values_list('follow', flat=True)) | Q(user_id=request.user))
    try:
        context['userinfo'] = UserInfo.objects.all()
    except ObjectDoesNotExist:
        # todo
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
        return redirect('/profile/' + request.user.username)
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

    new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'],
                                        email=request.POST['email'],
                                        first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                        is_active=False)
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
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return render(request, 'grumblr/404.html', context)
    try:
        tokens = RegToken.objects.filter(user_id=user, token=token)
        if (tokens.count() <= 0):
            return render(request, 'grumblr/404.html', context)
    except ObjectDoesNotExist:
        return render(request, 'grumblr/404.html', context)
    user.is_active = True
    user.save()
    context['message'] = "Verification success. Now, you can login to your Gumblr."
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


@login_required
def follow(request, username):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect('/profile/' + username)
    following = Following(user=request.user, follow=user)
    following.save()
    return redirect('/profile/' + username)


@login_required
def unfollow(request, username):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect('/profile/' + username)
    try:
        following = Following.objects.get(user=request.user, follow=user)
    except ObjectDoesNotExist:
        return redirect('/profile/' + username)
    following.delete()
    return redirect('/profile/' + username)


@login_required
def editprofile(request, username):
    context = {}
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return render(request, 'grumblr/404.html', context)
    try:
        userinfo = UserInfo.objects.get(user_id=user)
    except ObjectDoesNotExist:
        return render(request, 'grumblr/404.html', context)

    if request.method == 'GET':
        context['form'] = EditProfileForm(
            initial={'email': user.email, 'first_name': user.first_name,
                     'last_name': user.last_name})
        context['form2'] = AdditionalInfoForm(initial={'age': userinfo.age, 'short_bio': userinfo.short_bio})
        return render(request, 'grumblr/editprofile.html', context)

    form = EditProfileForm(request.POST)
    form2 = AdditionalInfoForm(request.POST, request.FILES, instance=userinfo)
    if not form.is_valid():
        context['form'] = form
        context['form2'] = form2
        return render(request, 'grumblr/editprofile.html', context)

    user.email = request.POST['email']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.set_password(request.POST['password1'])

    if not form2.is_valid:
        context['form'] = form
        context['form2'] = form2
        return render(request, 'grumblr/editprofile.html', context)
    form2.save()
    user.save()
    context['message'] = 'Edit profile success. Please login again.'
    return render(request, 'grumblr/loginpage.html', context)


def forgotpassword(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ForgotPasswordForm()
        return render(request, 'grumblr/forgotpassword.html', context)
    try:
        user = User.objects.get(username=request.POST['username'])
    except ObjectDoesNotExist:
        context['message'] = "Username does not exist."
        return render(request, 'grumblr/forgotpassword.html', context)

    token = default_token_generator.make_token(user)
    new_token = RegToken(user_id=user, token=token)
    new_token.save()

    email_body = """
    Please click the link below to change your password:

    http://%s%s 
    """ % (request.get_host(),
           reverse('resetpassword', args=(user.username, token)))

    send_mail(subject="Reset Password", message=email_body, from_email="nfajriya@andrew.cmu.edu",
              recipient_list=[user.email])

    return render(request, 'grumblr/requestsent.html')


def resetpassword(request, username, token):
    context = {}
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return render(request, 'grumblr/404.html', context)
    form = ResetPasswordForm()
    try:
        tokens = RegToken.objects.filter(user_id=user, token=token)
        if (tokens.count() <= 0):
            return render(request, 'grumblr/404.html', context)
    except ObjectDoesNotExist:
        return render(request, 'grumblr/404.html', context)
    context['form'] = form
    context['username'] = username
    context['token'] = token
    context['message'] = 'get'
    if request.method == 'GET':
        return render(request, 'grumblr/resetpassword.html', context)
    form = ResetPasswordForm(request.POST)
    if not form.is_valid():
        context['form'] = form
        context['message'] = 'not valid'
        return render(request, 'grumblr/resetpassword.html', context)

    user.set_password(request.POST['password1'])
    user.save()

    context['message'] = 'Reset password success. Please login again.'
    return render(request, 'grumblr/loginpage.html', context)

@login_required
def findusers(request):
    context = {}
    users = User.objects.order_by('username')
    context['users'] = users
    return render(request, 'grumblr/findusers.html', context)