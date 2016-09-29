from django.db import models


class Persona(models.Model):
    dni = models.IntegerField(primary_key=True, default=123456)
    nombre = models.CharField(max_length=100, default='John')
    apellido = models.CharField(max_length=100, default='Doe')
    direccion = models.CharField(max_length=100, default='Calle Falsa 123')
    telefono = models.IntegerField(default=123456)
    localidad = models.CharField(max_length=100, default='Neverland')

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)

    def _get_rol(self, klass):
        roles = list(filter(lambda r: isinstance(r, klass), self.roles))
        if roles:
            return roles[0]

    def _has_rol(self, klass):
        return self._get_rol(klass) is not None

    def add_rol(self, rol):
        if not self._has_rol(rol.__class__):
            rol.persona = self
            self.roles.append(rol)

    def __getattr__(self, attr):
        r = list(filter(lambda r: hasattr(r, attr), self.roles))
        if r:
            return getattr(r[0], attr)
"""
class Rol(models.Model):
    persona = models.ForeignKey(Persona, default=None)


class Cliente(Rol):
    email = models.EmailField(max_length=50, default='test@test.com')
    historial = []  # LISTA DE TURNOS (HISTORIAL)


    def sacar_turno(self):
        pass


class Empleado(Rol):
    porc_comicion = models.IntegerField()
    agenda = []  # LISTA DE TURNOS (AGENDA)

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

class Dueña(Rol):
    agenda = []  # LISTA DE TURNOS (AGENDA)

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

class Usuario(Rol):
    username = models.CharField(max_length=100, default='test')

    def login(self):
        pass
"""
