from django.db import models


class Persona(models.Model):
    dni = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.IntegerField()
    localidad = models.CharField(max_length=100)
    roles = []

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

class Rol(models.Model):
    persona = None


class Cliente(Rol):
    email = models.EmailField(max_length=50)
    historial = []  # LISTA DE TURNOS (HISTORIAL)


class Empleado(Rol):
    porc_comicion = models.IntegerField()
    agenda = []  # LISTA DE TURNOS (AGENDA)


class Usuario(Rol):
    pass
