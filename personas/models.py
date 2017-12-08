from django.contrib.auth.models import AbstractUser
from gestion.models import *
from datetime import datetime
from _datetime import date


class Rol(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        try:
            return '{} {}'.format(self.persona.nombre, self.persona.apellido)
        except AttributeError:
            return 'Rol no asignado'

class Cliente(Rol):
    email = models.EmailField(max_length=100, default='test@test.com')
    # historial = []  # LISTA DE TURNOS (HISTORIAL)

    def sacar_turno(self):
        print("sacando el turno")

class Empleado(Rol):
    porc_comision = models.PositiveIntegerField()
    sector = models.ForeignKey(Sector, null=True, blank=True)
    # agenda = []  # LISTA DE TURNOS (AGENDA)

    def alta_cliente(self):
        pass

    def reg_turno(self):
        pass

    def cancel_turno(self):
        pass

    def reg_turno_realizado(self):
        pass

    # TODOS LOS EMPLEADOS VAN A PODER MANEJAR TURNOS FIJOS? SINO HAY
    # QUE CREEAR EL ROL ESTETICISTA

    def reg_turno_fijo(self):
        pass

    def cancel_turno_fijo(self):
        pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def confirmar_turno(self):
        pass

    def modificar_turno(self, Turno):
        pass

    def modificar_stock_insumo(self):
        pass

    def horarios_disponibles(self):
        pass

    def reporte_turnos(self):
        pass

    def listar_servicios(self):
        pass

    def listar_historial_cliente(self, cliente):
        pass

    def get_pago(self, costo):
        comision = self.porc_comision
        pago = (costo*comision)/100
        return pago

class Duenia(Rol):
    # agenda = []  # LISTA DE TURNOS (AGENDA)

    def alta_sector(self):
        pass

    def reg_insumo(self):
        pass

    def reg_empleado(self):
        pass

    def reg_servicio(self):
        pass

    def mod_porcentaje_comision(self, empleado):
        pass

    def reporte_turnos(self):
        pass

    def servicios_mas_solicitados(self):
        pass

class Usuario(AbstractUser, Rol):

    def login(self):
        pass

    def get_vista(self):
        try:
            p = self.persona
            if p.duenia is not None:
                return 'duenio'
            elif p.empleado is not None:
                return 'empleado'
            elif p.cliente:
                return 'cliente'
        except models.ObjectDoesNotExist:
            pass
        return 'admin:index'


class Persona(models.Model):
    FILTROS = {
        "dni": ["dni__icontains"],
        "nombre": ["nombre__icontains"],
        "apellido": ["apellido__icontains"],
        "localidad": ["localidad__icontains"]
    }
    dni = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True)
    telefono = models.PositiveIntegerField(null=True)
    localidad = models.CharField(max_length=100, null=True)
    cliente = models.OneToOneField(Cliente, null=True, blank=True)
    empleado = models.OneToOneField(Empleado, null=True, blank=True)
    duenia = models.OneToOneField(Duenia, null=True, blank=True)
    usuario = models.OneToOneField(Usuario, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)

    def get_rol_url(self):
        if self.cliente:
            rol = 'cliente'
        if self.empleado:
            rol = 'empleado'
        if self.duenia:
            rol = 'duenio'
        return rol


class Comision(models.Model):
    FILTROS = {
        "empleadoN": ["turno__empleado__persona__nombre__icontains"],
        "empleadoA": [ "turno__empleado__persona__apellido__icontains"],
        "fechaI": ["fecha_liquidacion__gte"],
        "fechaF": ["fecha_liquidacion__lte"],
        "montoD": ["monto__gte"],
        "montoH": ["monto__lte"],
        "servicio": ["turno__servicios__nombre__icontains", "turno__promociones__nombre__icontains",
                     "turno__promociones__servicios__nombre__icontains"]
    }

    fecha_liquidacion = models.DateField(default=datetime.now)
    monto = models.FloatField(null=True)