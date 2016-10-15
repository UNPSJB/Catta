from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^empleado/$', views.empleado, name='empleado'),
    url(r'^nuevo_empleado/$', views.nuevo_empleado, name='nuevo_empleado'),
    url(r'^duenio/$', views.duenio, name='duenio'),
    url(r'^cuenta/$', views.cuenta, name='cuenta'),
    url(r'^cliente/$', views.cliente, name='cliente'),
    url(r'^nuevo_cliente/$', views.nuevo_cliente, name='nuevo_cliente'),
    url(r'^index_turnos/$', views.index_turnos, name='index_turnos'),
    url(r'^$', views.cerrar_sesion, name='cerrar_sesion')
]
