from django.forms import ModelForm
from turnos.models import Turno
from turnos.models import TurnoFijo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, Fieldset


class CrearTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrearTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_turno', 'Crear Turno'))
    class Meta:
        model = Turno
        fields={"fecha","empleado","servicios","cliente"}


class ModificarTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModificarTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('modificar_turno','Modificar Turno'))
    class Meta:
        model = Turno
        fields={"fecha","empleado","servicios"}

class ConfirmarTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConfirmarTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('confirmar_turno','Confirmar Turno'))
    class Meta:
        model = Turno
        fields={"fecha_confirmacion"}


class RegistrarTurnoRealizadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrarTurnoRealizadoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('confirmar_turno','Confirmar Turno'))
    class Meta:
        model = Turno
        fields = {"fecha", "empleado", "servicios","cliente"}