from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^altaSector/$', views.sector, name='altaSector'),
    url(r'^altaInsumo/$', views.insumo, name='altaInsumo'),
    url(r'^altaServicio/$', views.servicio, name='altaServicio'),
    url(r'^listaServicios/$', views.listaServicios, name='listaServicios'),
    url(r'^listaInsumos/$', views.listaInsumos, name='listaInsumos'),
    url(r'^modificarStockInsumo/(\d+)/$', views.modificarStockInsumo, name='modificarStockInsumo'),
    url(r'^modificar_servicio/(\d+)/$', views.modificar_servicio, name='modificar_servicio'),
    url(r'^eliminarInsumo/(\d+)/$', views.eliminarInsumo, name='eliminarInsumo'),
    url(r'^desactivar_promocion/(\d+)/$', views.desactivar_promocion, name='desactivar_promocion'),
    url(r'^activar_promocion/(\d+)/$', views.activar_promocion, name='activar_promocion'),
]
