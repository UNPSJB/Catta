from django.db import models

class Sector(models.Model):
    nombre = models.CharField(primary_key=True, max_length=100)
    descripcion = models.CharField(max_length=100)

class Insumo (models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    contenidoNeto = models.IntegerField(default=0)
    marca = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)

class Servicio (models.Model):
    nombre = models.CharField(primary_key=True, max_length=100)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField(default=0)
    duracion = models.IntegerField(default=0)
