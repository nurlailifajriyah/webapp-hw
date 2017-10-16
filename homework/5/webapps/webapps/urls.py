"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login

import grumblr.views


urlpatterns = [
    url(r'^$', grumblr.views.home),
    url(r'^admin', admin.site.urls),
    url(r'^loginsuccess/$', grumblr.views.loginsuccess),
    url(r'^globalstream$',grumblr.views.globalstream),
    url(r'^add-item/(?P<page>\w+)$',grumblr.views.add_item),
    url(r'^profile/(?P<username>\w+)$',grumblr.views.profile),
    url(r'^login$', login, {'template_name': 'grumblr/loginpage.html'}, name='login'),
    url(r'^logout$', logout_then_login),
    url(r'^register$', grumblr.views.register),
    url(r'^additionalinfo$', grumblr.views.additionalinfo),
    url(r'^confirm/(?P<username>\w+)/(?P<token>\S+)$', grumblr.views.confirm_registration, name='confirm_registration'),
    url(r'^follow/(?P<username>\w+)$',grumblr.views.follow),
    url(r'^unfollow/(?P<username>\w+)$',grumblr.views.unfollow),
    url(r'^editprofile/(?P<username>\w+)$',grumblr.views.editprofile),
    url(r'^forgotpassword$', grumblr.views.forgotpassword),
    url(r'^resetrequest/(?P<username>\w+)/(?P<token>\S+)$', grumblr.views.resetpassword, name='resetpassword'),
    url(r'^findusers/$', grumblr.views.findusers),
    url(r'^get-items/?$', grumblr.views.get_items),
    url(r'^get-items/(?P<time>.+)$', grumblr.views.get_items),
    url(r'^get-profile-items/(?P<username>\w+)$', grumblr.views.get_profile_items),
    url(r'^get-profile-items/(?P<username>\w+)/(?P<time>.+)$', grumblr.views.get_profile_items),



]
#source: https://docs.djangoproject.com/en/1.11/topics/http/views/
handler404 = 'grumblr.views.nofoundpage'
handler500 = 'grumblr.views.nofoundpage'
