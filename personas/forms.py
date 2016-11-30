from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, Form

from .models import Persona, Usuario, Cliente, Empleado, Comision
from gestion.models import Sector
from turnos.models import Turno
from datetime import date, time
from datetime import datetime


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

        if Usuario.objects.filter(username=self.cleaned_data['usuario']).exists():
            raise forms.ValidationError("Usuario en uso")

        if Persona.objects.filter(dni=self.cleaned_data['dni']).exists():
            raise forms.ValidationError("Esta persona ya se encuentra registrada en el sitio")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")

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

        if Usuario.objects.filter(username=self.cleaned_data['usuario']).exists():
            raise forms.ValidationError("Usuario en uso")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")

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

    def save(self, commit=True):
        comision = super(LiquidarComisionForm, self).save()

        fecha1 = datetime.combine(comision.fecha, time(00, 00, 00))
        fecha2 = datetime.combine(comision.fecha, time(20, 00, 00))
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
        fecha = datos.get('fecha')
        fecha1 = datetime.combine(fecha, time(00, 00, 00))
        fecha2 = datetime.combine(fecha, time(20, 00, 00))
        if Turno.objects.filter(empleado=empleado, fecha__range=[fecha1, fecha2], fecha_realizacion__range=[fecha1, fecha2]).count() == 0:
            raise forms.ValidationError("No hay turnos para liquidar en esta fecha para este empleado")

    class Meta:
        model = Comision
        fields = ("empleado","fecha_liquidacion")

