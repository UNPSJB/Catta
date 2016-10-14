from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, Fieldset, Field

from personas.models import Persona, Usuario, Cliente, Empleado, Duenia


class CuentaNuevaForm(forms.ModelForm):
    """
    Para crear clientes desde el formulario de "Cuenta Nueva" de la página principal.
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

        return p

    def clean(self):
        datos = super(CuentaNuevaForm, self).clean()

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


class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('iniciar_sesion', 'Iniciar Sesión'))

    class Meta:
        model = Usuario
        fields = ('username', 'password')

    """

    user = authenticate(username='john', password='secret')
    """