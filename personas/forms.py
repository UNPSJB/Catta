from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, Form

from .models import Persona, Usuario, Cliente, Empleado
from gestion.models import Sector


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


class LiquidarComisionForm(Form):

    empleado = forms.ModelChoiceField(queryset=Empleado.objects.all(), empty_label=" ")
    fecha = forms.DateField('%Y-$m-$d')

    def __init__(self, *args, **kwargs):
        super(LiquidarComisionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('liquidar_comision', 'Liquidar Comision'))

