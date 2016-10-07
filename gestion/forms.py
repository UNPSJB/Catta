from django.forms import ModelForm
from gestion.models import Sector
from gestion.models import Insumo
from gestion.models import Servicio

# Create the form class.
class SectorForm(ModelForm):
    class Meta:
        model = Sector
        fields={"nombre","descripcion"}

class InsumoForm(ModelForm):
    class Meta:
        model = Insumo
        fields = {"id", "nombre", "contenidoNeto", "marca", "stock"}

class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        fields = {"nombre", "descripcion", "precio", "duracion", "insumos"}