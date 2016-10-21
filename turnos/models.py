import datetime
from django.db import models
from gestion.models import *
from personas.models import *


class Turno(models.Model):
    fecha = models.DateTimeField()  # Fecha en la que se realizara el turno.
    fecha_creacion = models.DateTimeField(null=True, default=datetime.datetime.now)
    fecha_confirmacion = models.DateTimeField(null=True)
    fecha_realizacion = models.DateTimeField(null=True)
    fecha_cancelacion = models.DateTimeField(null=True)
    servicios = models.ManyToManyField(Servicio)
    empleado = models.ForeignKey(Empleado)
    cliente = models.ForeignKey(Cliente)

    def estado (self):
        if fecha_realizacion is not None:
            return "Realizado"
        else:
            if fecha_confirmacion is not None:
                return "Confirmado"
            else:
                if fecha_cancelacion is not None:
                    return "Cancelado"
                else:
                    return "Sin Confirmar"

    def cancelar_turno(self):
        fecha_cancelacion = datetime.datetime.now()

    def agregar_servicio(self):
        pass

    def eliminar_servicio(self):
        pass


class TurnoFijo(Turno):
    #ATRIBUTO DIA (EJEMPLO: Turno fijo los JUEVES) PUEDE SER ENUMERADO
    turno_siguiente = models.OneToOneField('self', null=True)
    fecha_fin = models.DateTimeField()

    def calcular_turno_siguiente(self):
        pass
