from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^empleado/$', views.empleado, name='empleado'),
    url(r'^nuevo_empleado/$', views.nuevo_empleado, name='nuevo_empleado'),
    url(r'^duenio/$', views.duenio, name='duenio'),
    url(r'^duenio_lista_empleados/$', views.duenio_lista_empleados, name='duenio_lista_empleados'),
    url(r'^duenio_lista_clientes/$', views.duenio_lista_clientes, name='duenio_lista_clientes'),
    url(r'^cuenta/$', views.cuenta, name='cuenta'),
    url(r'^cliente/$', views.cliente, name='cliente'),
    url(r'^$', views.cerrar_sesion, name='cerrar_sesion')
]
