from django.forms import ModelForm
from turnos.models import Turno
from turnos.models import TurnoFijo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, Fieldset

# Create the form class.
class TurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'id': 'TestIdForm', 'autocomplete': "off"}
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_turno', 'Crear Turno'))
    class Meta:
        model = Turno
        fields={"fecha","empleado","servicios","cliente"}


