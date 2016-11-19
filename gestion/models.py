from django.db import models
from datetime import timedelta


class Sector(models.Model):
    nombre = models.CharField(primary_key=True, max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.nombre)


class Insumo (models.Model):
    FILTROS = {
        "nombre": ["nombre__icontains"],
        "marca": ["marca__icontains"]
    }
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    contenidoNeto = models.PositiveIntegerField(default=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return "{} {}".format(self.nombre, self.marca)


class Servicio(models.Model):
    FILTROS = {
        "nombre": ["nombre__icontains"],
    }

    class Meta:
        abstract = True

    MODULO = timedelta(minutes=15)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField(default=0)
    sector = models.ForeignKey(Sector)

    def __str__(self):
        return "{}".format(self.nombre)


class ServicioBasico(Servicio):
    duracion = models.IntegerField(default=0)
    insumos = models.ManyToManyField(Insumo, blank=True)

    def get_duracion(self):
        return self.duracion * self.MODULO

    def get_nombre(self):
        return str(self.nombre)


class Promocion(Servicio):
    servicios = models.ManyToManyField(ServicioBasico)
    imagen = models.ImageField(upload_to='img_promocion',
                               null=True, blank=True,
                               width_field="alto_imagen",
                               height_field="ancho_imagen")
    alto_imagen = models.IntegerField(default=0)
    ancho_imagen = models.IntegerField(default=0)

    def get_duracion(self):
        duracion = 0

        for servicio in self.servicios.all():
            duracion += servicio.duracion

        return duracion * self.MODULO

    def get_nombre(self):
        return str(self.nombre)
