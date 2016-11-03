from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^modificar/$', views.modificar_turno, name='modifciar_turno'),
    url(r'^escupoJSON/$', views.escupoJSON, name='escupoJSON'),
    url(r'^devuelvo_turnos$', views.devuelvo_turnos, name='devuelvo_turnos'),
    url(r'^confirmarTurno$', views.confirmarTurno, name='confirmarTurno')
]
