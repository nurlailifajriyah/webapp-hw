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
    url(r'^admin/', admin.site.urls),
    url(r'^loginsuccess/', grumblr.views.loginsuccess),
    url(r'^globalstream$',grumblr.views.globalstream),
    url(r'^add-item',grumblr.views.add_item),
    url(r'^profile/(?P<username>\w+)$',grumblr.views.profile),
    # route to auth
    url(r'^login$', login, {'template_name': 'grumblr/loginpage.html'}, name='login'),
    url(r'^logout$', logout_then_login),
    url(r'^register$', grumblr.views.register),
    url(r'^additionalinfo$', grumblr.views.additionalinfo),
    url(r'^confirm/(?P<username>\w+)/(?P<token>\S+)$', grumblr.views.confirm_registration, name='confirm_registration'),
]
#source: https://docs.djangoproject.com/en/1.11/topics/http/views/
handler404 = 'grumblr.views.nofoundpage'
handler500 = 'grumblr.views.nofoundpage'
