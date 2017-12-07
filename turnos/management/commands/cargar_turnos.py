from django.core.management.base import BaseCommand
from datetime import timedelta, datetime, time
from personas.models import Empleado, Cliente
from gestion.models import ServicioBasico, Promocion
from turnos.models import Turno
import random

def rango_de_fechas(fecha_inicio, fecha_fin):
    for n in range(int ((fecha_fin - fecha_inicio).days)):
        yield fecha_inicio + timedelta(days=n)

def es_laborable(dia):
    return dia.weekday() in [1,2,3,4,5,6]


def cliente_random():
    clientes = Cliente.objects.all()
    indice = random.randint(0,5)
    return clientes[indice]


def get_servicios_random(empleado):
    servicios = ServicioBasico.objects.filter(sector=empleado.sector)
    indice = random.randint(0,len(servicios)-1)
    return servicios[indice]

def get_promociones(dia, empleado):
    promocion = Promocion.objects.filter(sector=empleado.sector)
    opcion = random.randint(0,1)
    if opcion == 0:
        return None
    else:
        return promocion[random]

def get_fecha(dia, servicios):
    opcion = random.randint(0,1)
    if opcion == 0:
        return None, dia
    else:
        return dia + servicios.get_duracion, None


def generar_turno(dia, empleado):
    turno = Turno()
    if not es_laborable(dia + timedelta(days=1)):
        dia_realizacion = dia + timedelta(days=2)
    else:
        dia_realizacion = dia + timedelta(days=1)

    turno.fecha = dia_realizacion #Esto me puede dejar el lunes como dia de realización del turno
    turno.dia = dia_realizacion.date()
    turno.hora = dia_realizacion.time()
    turno.fecha_creacion = dia
    fecha_confirmacion = dia
    turno.empleado = empleado
    turno.cliente = cliente_random()#Pueden repetirse ¡Ojo!
    turno.save()
    turno.servicios = get_servicios_random(empleado)
    turno.fecha_realizacion, turno.fecha_cancelacion = get_fecha(dia_realizacion, turno.servicios)
    #turno.promociones = get_promociones(dia, empleado)
    turno.comision = None
    turno.save()
    

class Command(BaseCommand):
    """
    Comando que 'Carga turnos durante el año 2016 utilizando los clientes y los servicios actuales'
    Modo de utilización python manage.py cargar_turnos
    """
    help = 'Carga los turnos duarente el año 2016 utilizando los clientes y los servicios actuales'
    #9-13 y de 16-20
    def handle(self, *args, **options):        
        fecha_inicio = datetime(2017, 1, 1)
        fecha_fin = datetime.today()
        for dia_actual in rango_de_fechas(fecha_inicio, fecha_fin):
            if es_laborable(dia_actual):
                for empleado in Empleado.objects.all():
                    #Un Turno a la mañana
                    generar_turno(dia_actual.replace(hour=9),empleado)
                    #Uno a la tarde
                    generar_turno(dia_actual.replace(hour=16),empleado)

                    