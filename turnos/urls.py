from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^modificar/$', views.modificar_turno, name='modifciar_turno'),
    url(r'^escupoJSON/$', views.escupoJSON, name='escupoJSON'),
    url(r'^devuelvo_turnos/$', views.devuelvo_turnos, name='devuelvo_turnos'),
    url(r'^devuelvo_turnos_libres/$', views.devuelvo_turnos_libres, name='devuelvo_turnos_libres'),
    #url(r'^listaTurnosFecha/$', views.listaTurnosFecha, name='listaTurnosFecha'),
    url(r'^calendario/$', views.calendario, name='calendario'),
    # url(r'^detalle_turno/$', views.detalle_turno, name='detalle_turno'),
    url(r'^confirmar_turno/(\d+)/$', views.confirmar_turno, name='confirmar_turno'),
    url(r'^modificar_turno/(\d+)/$', views.modificar_turno, name='modificar_turno'),
    url(r'^cancelar_turno/(\d+)/$', views.cancelar_turno, name='cancelar_turno'),
    url(r'^marcar_realizado/(\d+)/$', views.marcar_realizado, name='marcar_realizado'),
    url(r'^calendario/$', views.calendario, name='calendario')
]
