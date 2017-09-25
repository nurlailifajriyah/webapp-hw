from django.conf.urls import url, include
from sio.views import home

urlpatterns = [
    url(r'^sio/', include('sio.urls')),
    url(r'^$', home),
]
