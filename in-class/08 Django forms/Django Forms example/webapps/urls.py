from django.conf.urls import include, url
from private_todo_list.views import home

urlpatterns = [
    url(r'^private-todo-list/', include('private_todo_list.urls')),
    url(r'^$', home),
]
