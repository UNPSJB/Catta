from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^altaSector/$',views.sector, name='altaSector'),
    url(r'^altaInsumo/$', views.insumo, name='altaInsumo'),
    url(r'^altaServicio/$', views.servicio, name='altaServicio'),
    url(r'^listaServicios/$', views.listaServicios, name='listaServicios'),

]
