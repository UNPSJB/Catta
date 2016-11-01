from django.db import models
from datetime import timedelta


class Sector(models.Model):
    nombre = models.CharField(primary_key=True, max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.nombre)


class Insumo (models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    contenidoNeto = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return "{} {}".format(self.nombre, self.marca)


class ServicioManager(models.Manager):
    def __init__(self, promocion):
        super().__init__()
        self.promocion = promocion

    def get_queryset(self):
        return super().get_queryset().filter(promocion=self.promocion)


class Servicio(models.Model):
    MODULO = timedelta(minutes=15)
    nombre = models.CharField(primary_key=True, max_length=100)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField(default=0)
    duracion = models.IntegerField(default=0)
    insumos = models.ManyToManyField(Insumo)
    sector = models.ForeignKey(Sector, null=True, blank=True)
    servicios = models.ManyToManyField('self')
    promocion = models.BooleanField(default=False)
    objects = models.Manager()
    basicos = ServicioManager(False)
    promociones = ServicioManager(True)

    def __str__(self):
        return "{}".format(self.nombre)
