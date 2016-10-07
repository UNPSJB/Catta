from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):

    class Meta:
        abstract = True


class Cliente(Rol):
    email = models.EmailField(max_length=50, default='test@test.com')
    #historial = []  # LISTA DE TURNOS (HISTORIAL)


    def sacar_turno(self):
        print ("sacando el turno")


class Empleado(Rol):
    porc_comicion = models.IntegerField()
    #agenda = []  # LISTA DE TURNOS (AGENDA)

    def alta_cliente(self):
        pass

    def reg_turno(self):
        pass

    def cancel_turno(self):
        pass

    def reg_turno_realizado(self):
        pass

    #TODOS LOS EMPLEADOS VAN A PODER MANEJAR TURNOS FIJOS? SINO HAY
    #QUE CREEAR EL ROL ESTETICISTA

    def reg_turno_fijo(self):
        pass

    def cancel_turno_fijo(self):
        pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def confirmar_turno(self):
        pass

    def modificar_turno(self):
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

class Duenia(Rol):
    #agenda = []  # LISTA DE TURNOS (AGENDA)

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
"""
class Usuario(Rol):

    def login(self):
        pass
    """

class Persona(models.Model):
    dni = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True)
    telefono = models.IntegerField(null=True)
    localidad = models.CharField(max_length=100, null=True)
    cliente = models.OneToOneField(Cliente, null=True)
    empleado = models.OneToOneField(Empleado, null=True)
    Duenia = models.OneToOneField(Duenia, null=True)
    #usuario = models.OneToOneField(Usuario)

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)