from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ayuda_externa', views.ayuda_externa, name='ayuda_externa'),
    # Cuenta nueva.
    url(r'^cuenta/$', views.cuenta, name='cuenta'),
    # Vista del cliente.
    url(r'^ayuda_cliente/', views.ayuda_cliente, name='ayuda_cliente'),
    url(r'^cliente/$', views.cliente, name='cliente'),
    url(r'^nuevo_empleado/$', views.nuevo_empleado, name='nuevo_empleado'),  # TODO Ver si esto realmente es necesario.
    # Vista del empleado.
    url(r'^empleado/$', views.empleado, name='empleado'),
    url(r'^empleado/(\d+)/$', views.empleado, name='empleado'),
    url(r'^ayuda_empleado/', views.ayuda_empleado, name='ayuda_empleado'),
    # Listados de la vista del empleado.
    url(r'^empleado_lista_clientes/$', views.empleado_lista_clientes, name='empleado_lista_clientes'),
    url(r'^empleado_lista_servicios$', views.empleado_lista_servicios, name='empleado_lista_servicios'),
    url(r'^empleado_lista_insumos$', views.empleado_lista_insumos, name='empleado_lista_insumos'),
    url(r'^empleado_lista_turnos/$', views.empleado_lista_turnos, name='empleado_lista_turnos'),
    # Vista de la dueña.
    url(r'^duenio/$', views.duenio, name='duenio'),
    url(r'^ayuda_duenio/', views.ayuda_duenio, name='ayuda_duenio'),
    # Listados de la vista de la dueña.
    url(r'^modificar_stock_duenio/(\d+)/$', views.modificar_stock_duenio, name='modificar_stock_duenio'),
    url(r'^duenio_lista_empleados/$', views.duenio_lista_empleados, name='duenio_lista_empleados'),
    url(r'^duenio_lista_clientes/$', views.duenio_lista_clientes, name='duenio_lista_clientes'),
    url(r'^duenio_lista_servicios$', views.duenio_lista_servicios, name='duenio_lista_servicios'),
    url(r'^duenio_lista_insumos$', views.duenio_lista_insumos, name='duenio_lista_insumos'),
    url(r'^duenio_lista_turnos/$', views.duenio_lista_turnos, name='duenio_lista_turnos'),
    url(r'^duenio_lista_turno_creado_fijo/(\d+)/$', views.duenio_lista_turno_creado_fijo, name='duenio_lista_turno_creado_fijo'),
    url(r'^duenio_lista_comisiones/$', views.duenio_lista_comisiones, name='duenio_lista_comisiones'),
    url(r'^modificarComision/(\d+)/$', views.modificarComision, name='modificarComision'),
    url(r'^duenio_agenda/$', views.agenda_duenio, name='agenda_duenio'),
    url(r'^cliente_agenda/$', views.agenda_cliente, name='agenda_cliente'),
    url(r'^empleado_agenda/$', views.agenda_empleado, name='agenda_empleado'),
    url(r'^crear_turno/$', views.crear_turno_cliente, name='crear_turno'),
    url(r'^cliente_lista_servicios$', views.cliente_lista_servicios, name='cliente_lista_servicios'),
    url(r'^modificarComision/(\d+)/$', views.modificarComision, name='modificarComision'),
    url(r'^cliente_lista_turnos/$', views.cliente_lista_turnos, name='cliente_lista_turnos'),
    url(r'^restringido/$', views.restringido, name='restringido'),
    url(r'^ingreso_neto/$', views.ingreso_neto, name='ingreso_neto'),
    url(r'^servicios_mas_solicitados/$', views.servicios_mas_solicitados, name='servicios_mas_solicitados'),
    url(r'^mes_mayor_trabajo/$', views.mes_mayor_trabajo, name='mes_mayor_trabajo'),
    url(r'^dia_mayor_trabajo/$', views.dia_mayor_trabajo, name='dia_mayor_trabajo'),
    url(r'^dias_mayor_creaciones_turnos/$', views.dias_mayor_creaciones_turnos, name='dias_mayor_creaciones_turnos'),
    url(r'^clientes_con_mas_ausencias/$', views.clientes_con_mas_ausencias, name='clientes_con_mas_ausencias'),
    url(r'^empleados_mas_solicitados/$', views.empleados_mas_solicitados, name='empleados_mas_solicitados'),
    url(r'^horarios_mas_solicitados/$', views.horarios_mas_solicitados, name='horarios_mas_solicitados'),
    url(r'^servicios_mas_solicitados/$', views.servicios_mas_solicitados, name='servicios_mas_solicitados'),
    url(r'^empleados_mas_solicitados/$', views.empleados_mas_solicitados, name='empleados_mas_solicitados'),
    # Reportes PDF
    url(r'^empleados_mas_solicitados_pdf/', views.EmpleadosMasSolicitadosPDF.as_view(), name="empleados_mas_solicitados_pdf"),
    # Cerrar Sesión.
    url(r'^$', views.cerrar_sesion, name='cerrar_sesion')

]
