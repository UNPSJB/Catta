from django.db import models

class Persona(models.Model):
    dni = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.IntegerField()
    localidad = models.CharField(max_length=100)

class Cliente(models.Model):
	email = models.EmailField(max_length=50)
	historial = []#LISTA DE TURNOS (HISTORIAL)

class Empleado(models.Model):
	porc_comicion = models.IntegerField()
	agenda = []#LISTA DE TURNOS (AGENDA)
