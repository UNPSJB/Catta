from personas.models import *
from django.utils import timezone
from django.db.models import Q, Sum, F
from django.conf import settings
from django.utils import timezone
import  enum
from datetime import date, time, timedelta, datetime

class TurnoBaseManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().annotate(servicio_modulos=Sum("servicios__duracion"))
        qs = qs.annotate(promocion_modulos=Sum("promociones__servicios__duracion"))
        return qs

class TurnoQuerySet(models.QuerySet):
    def en_dia(self, date):
        return self.filter(fecha__date = date)

    def en_estado(self, estado):
        return self.filter(Turno.FILTROS["estado"][estado])

TurnoManager = TurnoBaseManager.from_queryset(TurnoQuerySet)

def crear_rango(turno):
    r = []
    base = turno[0]
    while base <= turno[1]:
        r.append(base)
        base = (datetime.combine(date.today(), base) + settings.MODULO).time()
    return r

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
        "servicio": [ "servicios__nombre__icontains", "promociones__nombre__icontains", "promociones__servicios__nombre__icontains" ],
        "estado": {
            CANCELADO: Q(fecha_cancelacion__isnull = False),
            REALIZADO: Q(fecha_realizacion__isnull = False),
            CONFIRMADO: Q(fecha_confirmacion__isnull = False) & Q(fecha_realizacion__isnull = True) & Q(fecha_cancelacion__isnull = True),
            SIN_CONFIRMAR: Q(fecha_confirmacion__isnull = True) & Q(fecha_realizacion__isnull = True) & Q(fecha_cancelacion__isnull = True)
        }
    }
    #fecha se deja como esta pero a su vez se divide en dos atributos mas fecha sola y hora,
    #fecha creacion se le quita la hora. que dia se sacan mas turnos
    fecha = models.DateTimeField()  # Fecha en la que se realizara el turno.
    dia = models.DateField(default=date.today)
    hora = models.TimeField(default=timezone.now)
    # TIEMPO_MAX_CONFIRMACION = fecha - timedelta(days=2)  # Tiempo maximo de confirmación
    fecha_creacion = models.DateField(default=date.today)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    fecha_realizacion = models.DateTimeField(null=True, blank=True)
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    servicios = models.ManyToManyField(ServicioBasico, blank=True, related_name="turnos")
    promociones = models.ManyToManyField(Promocion, blank=True, related_name="turnos")
    empleado = models.ForeignKey(Empleado)
    cliente = models.ForeignKey(Cliente)
    objects = TurnoManager()
    comision = models.ForeignKey(Comision, null=True, blank=True)

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

    def get_proximo_turno(self, turno):

        fecha_turno = turno.fecha
        fecha_1 = fecha_turno.replace(hour=00, minute=00, second=00)
        fecha_2 = fecha_turno.replace(hour=20, minute=00, second=00)

        empleado = turno.empleado

        turnos = Turno.objects.filter(empleado=empleado, fecha__range=[fecha_1, fecha_2]).order_by('fecha')

        turno_sig = None

        if turnos != None:
            for turno_siguiente in turnos:
                fecha = turno_siguiente.fecha
                if fecha_turno < fecha:
                    turno_sig = turno_siguiente
                    return turno_sig

        return turno_sig

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
        self.fecha_cancelacion = datetime.now()

    def realizar_turno(self):
        self.fecha_realizacion = datetime.now()

    def confirmar_turno(self):
        self.fecha_confirmacion = datetime.now()

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

    def get_fecha(self):
        formato = "%d-%m-%y %I"
        return self.fecha.strftime(formato)

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
    fecha_fin = models.DateTimeField()
    #dia = models.CharField(max_length=9, choices=DIA, default='Martes')

    def calcular_turno_siguiente(self,f):
        print(f)
        fecha_nueva = f + timedelta(days=7)
        #fecha_1 = self.get_duracion()
        #formato = "%d-%m-%y"
        #fecha_1 = fecha_nueva
        #fecha_2 = fecha_nueva
        fecha_1 = fecha_nueva.replace(hour= 00, minute = 00, second = 00)
        fecha_2 = fecha_nueva.replace(hour = 20, minute = 00, second = 00)
        existe = Turno.objects.filter(empleado=self.empleado, fecha=fecha_nueva).exists()
        #existen = Turno.objects.filter(empleado=self.empleado)
        existen = Turno.objects.filter(empleado=self.empleado, fecha__range=[fecha_1, fecha_2])
        for e in existen:
            print ("hay existen")
            print(e)
            if e.get_fecha() == fecha_2:
                if (e.fecha < fecha_nueva and e.get_duracion() > fecha_nueva) or (fecha_nueva < e.fecha and e.fecha < self.get_duracion):
                    existe = True
                    break
        print(existe)
        if(self.fecha_fin > fecha_nueva):
            if (not existe):
                t = TurnoFijo()
                t.empleado = self.empleado
                t.fecha = fecha_nueva
                t.fecha_fin = self.fecha_fin
                t.cliente = self.cliente
                t.save()
                serv = self.servicios.all()
                for s in serv:
                    t.servicios.add(s)
                prom = self.promociones.all()
                for p in prom:
                    t.promociones.add(p)
                t.save()
                self.turno_siguiente = t
                print(self.turno_siguiente.fecha)
                t.calcular_turno_siguiente(t.fecha)
                self.save()
            else:
                print("no se creo turno")
                print(fecha_nueva)
                self.calcular_turno_siguiente(fecha_nueva)
