from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$',views.login),
    url(r'^empleado/$',views.empleado),
    url(r'^cuenta/$',views.cuenta),
]