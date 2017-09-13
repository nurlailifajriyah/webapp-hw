from django.conf.urls import url, include
import sio.views

urlpatterns = [
    url(r'^$', sio.views.home),
]
