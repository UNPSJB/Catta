
import datetime
from personas.models import *


class Turno(models.Model):
    fecha = models.DateTimeField()  # Fecha en la que se realizara el turno.
    # TIEMPO_MAX_CONFIRMACION = fecha - timedelta(days=2)  # Tiempo maximo de confirmación
    fecha_creacion = models.DateTimeField(null=True, default=datetime.datetime.now)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    fecha_realizacion = models.DateTimeField(null=True, blank=True)
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    servicios = models.ManyToManyField(ServicioBasico)
    promociones = models.ManyToManyField(Promocion)
    empleado = models.ForeignKey(Empleado)
    cliente = models.ForeignKey(Cliente)

    def __str__(self):
        return "{}".format(self.fecha)

    def get_duracion(self):
        servicios = self.servicios.all()
        duracion = self.fecha

        for servicio in servicios:
            duracion += servicio.get_duracion()
        return duracion

    def estado(self):
        if self.fecha_realizacion is not None:
            return "Realizado"
        else:
            if self.fecha_confirmacion is not None:
                return "Confirmado"
            else:
                if self.fecha_cancelacion is not None:
                    return "Cancelado"
                else:
                    return "Sin Confirmar"

    def cancelar_turno(self):
        self.fecha_cancelacion = datetime.datetime.now()

    def confirmar_turno(self):
        self.fecha_confirmacion = datetime.datetime.now()

    def agregar_servicio(self):
        pass

    def eliminar_servicio(self):
        pass


class TurnoFijo(Turno):
    # ATRIBUTO DIA (EJEMPLO: Turno fijo los JUEVES) PUEDE SER ENUMERADO
    turno_siguiente = models.OneToOneField('self', null=True)
    fecha_fin = models.DateTimeField()

    def calcular_turno_siguiente(self):
        pass
