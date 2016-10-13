from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, Fieldset
from personas.models import Persona
from personas.models import Usuario
from personas.models import Cliente
from personas.models import Empleado
from personas.models import Duenia


class CuentaNuevaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CuentaNuevaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_cuenta', 'Crear Cuenta'))

    class Meta:
        model = Persona
        fields = ("dni",
                  "nombre", "apellido",
                  "direccion", "telefono", "localidad")
