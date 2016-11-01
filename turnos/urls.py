from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^escupoJSON/$', views.escupoJSON, name='escupoJSON'),
    url(r'^modificar/$', views.modificar_turno, name='modifciar_turno'),
    url(r'^eventosCalendario/$', views.eventosCalendario, name='eventosCalendario')
]
