from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^escupoJSON/$', views.escupoJSON, name='escupoJSON'),
]
