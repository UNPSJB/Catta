from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, Form

from .models import Persona, Usuario, Cliente, Empleado, Comision
from gestion.models import Sector
from turnos.models import Turno
from datetime import date, time
from datetime import datetime

import re
from django.conf import settings

class CuentaNuevaForm(forms.ModelForm):
    """
    Para crear clientes desde el formulario de "Cuenta Nueva" de la página principal, desde la vista de dueña y empleado
    """
    email = forms.EmailField(max_length=100, label="E-Mail")
    usuario = forms.CharField(max_length=30)
    passwd = forms.CharField(max_length=30, widget=forms.PasswordInput, label='Contraseña')
    passwd_1 = forms.CharField(max_length=30, widget=forms.PasswordInput, label='Repita la contraseña')

    def __init__(self, *args, **kwargs):
        super(CuentaNuevaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_cuenta', 'Crear Cuenta'))

    def save(self, commit=True):
        p = super(CuentaNuevaForm, self).save()
        u = Usuario.objects.create_user(username=self.cleaned_data['usuario'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['passwd'])
        c = Cliente()
        c.email = self.cleaned_data['email']
        c.save()

        p.usuario = u
        p.cliente = c
        u.persona = p

        if commit:
            u.save()
            p.save()

        return p.usuario

    def clean(self):
        datos = super(CuentaNuevaForm, self).clean()

        p1 = datos.get('passwd')
        p2 = datos.get('passwd_1')
        dni = datos.get('dni')
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')
        telefono = datos.get('telefono')
        direccion = datos.get('direccion')
        localidad = datos.get('localidad')


        if Usuario.objects.filter(username=self.cleaned_data['usuario']).exists():
            raise forms.ValidationError("Usuario en uso")

        if Persona.objects.filter(dni=self.cleaned_data['dni']).exists():
            raise forms.ValidationError("Esta persona ya se encuentra registrada en el sitio")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        # Validación de datos del formulario (Tipos y rangos)
        if re.fullmatch(settings.RE_DNI, str(dni)) is None:
            raise forms.ValidationError("El dni ingresado es incorrecto")

        if re.match(settings.RE_LETRAS, nombre) is None:
            raise forms.ValidationError("El nombre es incorrecto")

        if re.match(settings.RE_LETRAS, apellido) is None:
            raise forms.ValidationError("El apellido es incorrecto")

        if re.fullmatch(settings.RE_TELEFONO, str(telefono)) is None:
            raise forms.ValidationError("El teléfono es incorrecto")

        if re.match(settings.RE_CARACTERES, str(direccion)) is None:
            raise forms.ValidationError("La dirección es incorrecta")

        if re.match(settings.RE_CARACTERES, str(localidad)) is None:
            raise forms.ValidationError("La localidad es incorrecta")

        return datos

    class Meta:
        model = Persona
        fields = ("dni",
                  "nombre", "apellido",
                  "direccion", "telefono", "localidad")


class EmpleadoNuevoForm(forms.ModelForm):
    """
    Para crear clientes desde el formulario de "Cuenta Nueva" de la página principal.
    """
    sector = forms.ModelChoiceField(queryset=Sector.objects.all(), empty_label="---------")
    comision = forms.FloatField(label="Porcentaje de comisión")
    email = forms.EmailField(max_length=100, label="E-Mail")
    usuario = forms.CharField(max_length=30)
    passwd = forms.CharField(max_length=30, widget=forms.PasswordInput, label='Contraseña')
    passwd_1 = forms.CharField(max_length=30, widget=forms.PasswordInput, label='Repita la contraseña')

    def __init__(self, *args, **kwargs):
        super(EmpleadoNuevoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_empleado', 'Crear Empleado'))

    def save(self, commit=True):
        p = super(EmpleadoNuevoForm, self).save()
        u = Usuario.objects.create_user(username=self.cleaned_data['usuario'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['passwd'])

        e = Empleado()
        e.sector = Sector.objects.get(nombre=self.cleaned_data['sector'])
        e.porc_comision = self.cleaned_data['comision']
        e.save()

        p.usuario = u
        p.empleado = e
        u.persona = p

        if commit:
            u.save()
            p.save()

        return p

    def clean(self):
        datos = super(EmpleadoNuevoForm, self).clean()

        p1 = datos.get('passwd')
        p2 = datos.get('passwd_1')
        c = datos.get('comision')
        dni = datos.get('dni')
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')
        telefono = datos.get('telefono')
        direccion = datos.get('direccion')
        localidad = datos.get('localidad')

        if c > 100 or c < 0:
            raise forms.ValidationError("El valor de la comision debe ser un pocentaje (entre 0 y 100)")

        if Usuario.objects.filter(username=self.cleaned_data['usuario']).exists():
            raise forms.ValidationError("Usuario en uso")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        if re.fullmatch(settings.RE_DNI, str(dni)) is None:
            raise forms.ValidationError("El dni ingresado es incorrecto")

        if re.match(settings.RE_LETRAS, nombre) is None:
            raise forms.ValidationError("El nombre es incorrecto")

        if re.match(settings.RE_LETRAS, apellido) is None:
            raise forms.ValidationError("El apellido es incorrecto")

        if re.fullmatch(settings.RE_TELEFONO, str(telefono)) is None:
            raise forms.ValidationError("El teléfono es incorrecto")

        if re.match(settings.RE_CARACTERES, str(direccion)) is None:
            raise forms.ValidationError("La dirección es incorrecta")

        if re.match(settings.RE_CARACTERES, str(localidad)) is None:
            raise forms.ValidationError("La localidad es incorrecta")

        return datos

    class Meta:
        model = Persona
        fields = ("dni",
                  "nombre", "apellido",
                  "direccion", "telefono", "localidad")


class LiquidarComisionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LiquidarComisionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('liquidar_comision', 'Liquidar Comision'))
    """
    def save(self, commit=True):
        comision = super(LiquidarComisionForm, self).save()

        fecha1 = datetime.combine(comision.fecha_liquidacion, time(00, 00, 00))
        fecha2 = datetime.combine(comision.fecha_liquidacion, time(20, 00, 00))
        turnos = Turno.objects.filter(empleado=comision.empleado, fecha__range=[fecha1, fecha2], fecha_realizacion__range=[fecha1, fecha2])
        costo = 0
        for turno in turnos:
            costo += turno.get_costo()

        comision.monto = comision.empleado.get_pago(costo)

        comision.save()

        return comision

    def clean(self):
        datos = super(LiquidarComisionForm, self).clean()

        empleado = datos.get('empleado')
        print (empleado)
        fecha = datos.get('fecha_liquidacion')
        fecha1 = datetime.combine(fecha, time(00, 00, 00))
        fecha2 = datetime.combine(fecha, time(20, 00, 00))
        if Turno.objects.filter(empleado=empleado, fecha__range=[fecha1, fecha2], fecha_realizacion__range=[fecha1, fecha2]).count() == 0:
            raise forms.ValidationError("No hay turnos para liquidar en esta fecha para este empleado")
    """
    class Meta:
        model = Comision
        fields = ("fecha_liquidacion",)
