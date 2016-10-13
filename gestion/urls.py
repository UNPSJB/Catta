from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^sector/$',views.sector, name='sector'),
    url(r'^insumo/$', views.insumo, name='insumo'),
    url(r'^servicio/$', views.servicio, name='servicio'),
    url(r'^listaServicios/$', views.listaServicios, name='listaServicios'),

]
