from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$',views.login, name='login'),
    url(r'^empleado/$',views.empleado, name='empleado'),
    url(r'^duenio/$', views.duenio, name='duenio'),
    url(r'^cuenta/$',views.cuenta, name='cuenta'),
    url(r'^sector/$',views.sector, name='sector'),
    url(r'^cliente/$', views.cliente, name='cliente'),
]
