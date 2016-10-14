from django.db import models

class Sector(models.Model):
    nombre = models.CharField(primary_key=True, max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.nombre)

class Insumo (models.Model):
    nombre = models.CharField(max_length=100)
    contenidoNeto = models.IntegerField(default=0)
    marca = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    def __str__(self):
        return "{} {}".format(self.nombre, self.marca)

class Servicio (models.Model):
    nombre = models.CharField(primary_key=True, max_length=100)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField(default=0)
    duracion = models.IntegerField(default=0)
    insumos = models.ManyToManyField(Insumo)
    sector = models.ForeignKey(Sector, null=True, blank=True)
    servicios = models.ManyToManyField('self')

    def __str__(self):
        return "{}".format(self.nombre)