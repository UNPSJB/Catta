from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^sector/$',views.sector, name='sector'),
]
