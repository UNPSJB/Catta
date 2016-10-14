from django.forms import ModelForm
from gestion.models import Sector
from gestion.models import Insumo
from gestion.models import Servicio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, Fieldset


# Create the form class.
class SectorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_sector', 'Crear Sector'))

    class Meta:
        model = Sector
        fields={"nombre","descripcion"}

class InsumoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(InsumoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_insumo', 'Crear Insumo'))

    class Meta:
        model = Insumo
        fields = {"id", "nombre", "contenidoNeto", "marca", "stock"}

class ServicioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_servicio', 'Crear Servicio'))

    class Meta:
        model = Servicio
        fields = {"nombre", "descripcion", "precio", "duracion", "insumos"}



