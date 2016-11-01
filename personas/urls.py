from django.conf.urls import url
from . import views

urlpatterns = [
    # Cuenta nueva.
    url(r'^cuenta/$', views.cuenta, name='cuenta'),
    # Vista del cliente.
    url(r'^cliente/$', views.cliente, name='cliente'),
    url(r'^nuevo_empleado/$', views.nuevo_empleado, name='nuevo_empleado'),  # TODO Ver si esto realmente es necesario.
    # Vista del empleado.
    url(r'^empleado/$', views.empleado, name='empleado'),
    # Listados de la vista del empleado.
    url(r'^empleado_lista_clientes/$', views.empleado_lista_clientes, name='empleado_lista_clientes'),
    url(r'^empleado_lista_servicios$', views.empleado_lista_servicios, name='empleado_lista_servicios'),
    url(r'^empleado_lista_insumos$', views.empleado_lista_insumos, name='empleado_lista_insumos'),
    # Vista de la dueña.
    url(r'^duenio/$', views.duenio, name='duenio'),
    # Listados de la vista de la dueña.
    url(r'^duenio_lista_empleados/$', views.duenio_lista_empleados, name='duenio_lista_empleados'),
    url(r'^duenio_lista_clientes/$', views.duenio_lista_clientes, name='duenio_lista_clientes'),
    url(r'^duenio_lista_servicios$', views.duenio_lista_servicios, name='duenio_lista_servicios'),
    url(r'^duenio_lista_insumos$', views.duenio_lista_insumos, name='duenio_lista_insumos'),
    # Cerrar Sesión.
    url(r'^$', views.cerrar_sesion, name='cerrar_sesion')
]
