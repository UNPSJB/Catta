from django.db import models

class Sector(models.Model):
    nombre = models.CharFIeld(max_length=100)
    descripcion = models.CharFIeld(max_lenght=100)

class Insumo
    nombre = models.CharFIeld(max_length=100)
    contenidoNeto = models.IntegerField(default=0)
    marca = models.CharFIeld(max_length=100)
    stock = models.IntegerField(default=0)

class Servicio
    nombre = models.CharFIeld(max_length=100)
    descripcion = models.CharFIeld(max_length=100)
    precio = models.IntegerField(default=0)
    duracion = models.IntegerField(default=0)
