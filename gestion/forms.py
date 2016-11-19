from django.forms import ModelForm
from django import forms
from .models import Sector
from .models import Insumo
from .models import ServicioBasico, Promocion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class SectorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_sector', 'Crear Sector'))

    class Meta:
        model = Sector
        fields = {"nombre", "descripcion"}


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
        model = ServicioBasico
        fields = {"sector", "nombre", "descripcion", "precio", "duracion", "insumos"}


class PromoForm(ModelForm):
    servicios = forms.ModelMultipleChoiceField(queryset = ServicioBasico.objects.all())

    def __init__(self, *args, **kwargs):
        super(PromoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_promo', 'Crear Promo'))

        """
        La duracion de la promo y los insumos se sacan de los servicios que la componen.
        """

    class Meta:
        model = Promocion
        fields = ("nombre", "descripcion", "precio", "sector", "servicios", "imagen")
