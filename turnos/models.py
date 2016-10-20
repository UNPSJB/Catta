from django.db import models
from gestion.models import *

class Turno(models.Model):
    fecha = models.DateTimeField()
    origen = models.CharField(max_length=50)
    fecha_creacion= models.DateTimeField()
    fecha_confirmacion = models.DateTimeField()
    fecha_realizacion = models.DateTimeField()
    realizado = models.BooleanField()
    servicios = models.ManyToManyField(Servicio)

    SIN_CONFIRMAR = 'SC'
    CONFIRMADO = 'CO'
    REALIZADO = 'RE'
    CANCELADO = 'CA'
    ESTADO_TURNO = (
        (SIN_CONFIRMAR, 'Sin_Confirmar'),
        (CONFIRMADO, 'Confirmado'),
        (REALIZADO, 'Realizado'),
        (CANCELADO, 'Cancelado'),
    )

    estado = models.CharField(
        max_length=2,
        choices=ESTADO_TURNO,
        default=SIN_CONFIRMAR,
    )

    def agregar_servicio(self):
        pass

    def eliminar_servicio(self):
        pass

class TurnoFijo(Turno):
    #ATRIBUTO DIA (EJEMPLO: Turno fijo los JUEVES) PUEDE SER ENUMERADO
    turno_siguiente = models.OneToOneField(TurnoFijo)
    fecha_fin = models.DateTimeField()

    def calcular_turno_siguiente(self):
        pass
