import datetime
from personas.models import *
from django.db.models import Q
import  enum
from datetime import date, time, timedelta

class Turno(models.Model):
    CONFIRMADO = 2
    CANCELADO = 0
    SIN_CONFIRMAR = 1
    REALIZADO = 3
    ESTADOS = [
        (CANCELADO, "Cancelado"),
        (SIN_CONFIRMAR, "Sin Confirmar"),
        (CONFIRMADO, "Confirmado"),
        (REALIZADO, "Realizado")
    ]
    FILTROS = {
        "fechaI": ["fecha__date__gte"],
        "fechaF": ["fecha__date__lte"],
        "clienteN": [ "cliente__persona__nombre__icontains"],
        "clienteA": ["cliente__persona__apellido__icontains"],
        "empleadoN": ["empleado__persona__nombre__icontains"],
        "empleadoA": [ "empleado__persona__apellido__icontains"],
        "servicio": [ "servicios__nombre__icontains" ],
        "estado": {
            CANCELADO: Q(fecha_cancelacion__isnull = False),
            REALIZADO: Q(fecha_realizacion__isnull = False),
            CONFIRMADO: Q(fecha_confirmacion__isnull = False) & Q(fecha_realizacion__isnull = True) & Q(fecha_cancelacion__isnull = True),
            SIN_CONFIRMAR: Q(fecha_confirmacion__isnull = True) & Q(fecha_realizacion__isnull = True) & Q(fecha_cancelacion__isnull = True)
        }
    }
    fecha = models.DateTimeField()  # Fecha en la que se realizara el turno.
    # TIEMPO_MAX_CONFIRMACION = fecha - timedelta(days=2)  # Tiempo maximo de confirmación
    fecha_creacion = models.DateTimeField(null=True, default=datetime.now)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    fecha_realizacion = models.DateTimeField(null=True, blank=True)
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    servicios = models.ManyToManyField(ServicioBasico, blank=True, related_name="turnos")
    promociones = models.ManyToManyField(Promocion, blank=True, related_name="turnos")
    empleado = models.ForeignKey(Empleado)
    cliente = models.ForeignKey(Cliente)
    objects = TurnoManager()

    def __str__(self):
        return "{}".format(self.fecha)

    @classmethod
    def posibles_turnos(cls, fecha, servicios=None, promociones=None, usuario=None):
        delta = timedelta(minutes=0)
        turnos = cls.objects.en_dia(fecha).en_estado(not Turno.CANCELADO)
        if usuario is not None:
            turnos = turnos.filter(empleado=usuario)
        if servicios is not None:
            for servicio in servicios:
                delta += ServicioBasico.objects.all().filter(id=servicio).first().get_duracion()
        if promociones is not None:
            for promocion in promociones:
                delta += Promocion.objects.all().filter(id=promocion).first().get_duracion()
        # Crea el set con todos los horarios del día.
        rango = set(crear_rango(settings.MAÑANA) + crear_rango(settings.TARDE))
        # Si el día elegido es hoy, elimina los horarios anteriores a la hora actual.
        if fecha == datetime.today().date():
            for r in reversed(sorted(rango)):
                if r <= datetime.today().time():
                    rango.remove(r)
        # Saca del set de horarios los que sobrepasan el tamaño del turno a crear.
        rango = rango.difference(crear_rango((
            (datetime.combine(date.today(), settings.TARDE[1]) - delta).time(),
            settings.TARDE[1])))
        for t in turnos:
            r = crear_rango((t.fecha.time(), (t.fecha + t.duracion()).time()))
            rango = rango.difference(r)

        return sorted(rango)

    def duracion(self):
        return ((self.servicio_modulos or 0) +
                (self.promocion_modulos or 0)) * settings.MODULO

    def get_cliente(self):
        return str(self.cliente)

    def get_empleado(self):
        return str(self.empleado)

    def get_servicios(self):
        servicios = self.servicios.all()
        nombres = ""
        for servicio in servicios:
            nombres += servicio.get_nombre()
        return str(nombres)

    def get_promociones(self):
        promociones = self.promociones.all()
        nombres = ""
        for promocion in promociones:
            nombres += promocion.get_nombre()
        return str(nombres)

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
            if self.fecha_cancelacion is not None :
                return "Cancelado"
            else:
                if self.fecha_confirmacion is not None:
                    return "Confirmado"
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

    def get_costo(self):
        costo = 0
        for servicio in  self.servicios.all():
            costo += servicio.precio
        for promociones in self.promociones.all():
            costo += promociones.precio

        return costo

class TurnoFijo(Turno):
    MARTES ='Martes'
    MIERCOLES ='Miercoles'
    JUEVES ='Jueves'
    VIERNES ='Viernes'
    SABADO ='Sabado'
    DIA = [
        (MARTES, 'Martes'),
        (MIERCOLES, 'Miercoles'),
        (JUEVES, 'Jueves'),
        (VIERNES, 'Viernes'),
        (SABADO, 'Sabado')
    ]
    # ATRIBUTO DIA (EJEMPLO: Turno fijo los JUEVES) PUEDE SER ENUMERADO
    #turno_siguiente = models.OneToOneField('self',null=True, blank=True,default=self.calcular_turno_siguiente())
    turno_siguiente = models.OneToOneField('self', null=True)
    fecha_fin = models.DateTimeField(null=True,blank=True)
    #dia = models.CharField(max_length=9, choices=DIA, default='Martes')

    def calcular_turno_siguiente(self):
        print(self.fecha_fin)
        if self.fecha_fin < self.fecha + timedelta(days=7):
            t = TurnoFijo()
            t.empleado = self.empleado
            t.fecha = self.fecha + timedelta(days=7)
            t.servicios = self.servicios
            t.promociones = self.promociones
            t.cliente = self.cliente
            self.turno_siguiente = t
            #t.calcular_turno_siguiente()

#class Dia(enum):
 #   martes=1
  #  miercoles=2
   ##viernes=4
    #sabado=5
