import re
from django.forms import ModelForm
from django import forms
from .models import Sector
from .models import Insumo
from .models import ServicioBasico, Promocion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.conf import settings


class SectorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_sector', 'Crear Sector'))

    def clean(self):
        datos = super(SectorForm, self).clean()

        nombre = datos.get('nombre')
        descripcion = datos.get('descripcion')

        if re.match(settings.RE_CARACTERES, nombre) is None:
            raise forms.ValidationError("El nombre es incorrecto")

        if re.match(settings.RE_CARACTERES, descripcion) is None:
            raise forms.ValidationError("La descripcion es incorrecta")

        return datos

    class Meta:
        model = Sector
        fields = {
            "nombre",
            "descripcion"
        }


class InsumoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(InsumoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_insumo', 'Crear Insumo'))

    def clean(self):
        datos = super(InsumoForm, self).clean()

        cn = datos.get('contenidoNeto')
        s = datos.get('stock')
        nombre = datos.get('nombre')

        if cn <= 0:
            raise forms.ValidationError("El contenido neto del insumo ingresado es incorrecto")

        if s < 0:
            raise forms.ValidationError("El stock ingresado no puede ser negativo")

        if re.match(settings.RE_CARACTERES, nombre) is None:
            raise forms.ValidationError("El nombre es incorrecto")

        return datos

    class Meta:
        model = Insumo
        fields = {
            "id",
            "nombre",
            "contenidoNeto",
            "unidadDeMedida",
            "marca",
            "stock"
        }


class ServicioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_servicio', 'Crear Servicio'))

    def clean(self):
        datos = super(ServicioForm, self).clean()

        p = datos.get('precio')
        nombre = datos.get('nombre')
        descripcion = datos.get('descripcion')


        if p <= 0:
            raise forms.ValidationError("El precio del servicio no puede ser menor a $0")

        d = datos.get('duracion')
        if d <= 0:
            raise forms.ValidationError("La duracion del servicio debe ser como minimo de 1 modulo")

        if re.match(settings.RE_CARACTERES, nombre) is None:
            raise forms.ValidationError("El nombre es incorrecto")

        if re.match(settings.RE_CARACTERES, descripcion) is None:
            raise forms.ValidationError("La descripcion es incorrecta")

        return datos

    class Meta:
        model = ServicioBasico
        fields = {
            "sector",
            "nombre",
            "descripcion",
            "precio",
            "duracion",
            "insumos"
        }


class ModificarServicioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModificarServicioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('modificar_servicio', 'Modificar Servicio'))

    def clean(self):
        datos = super(ModificarServicioForm, self).clean()

        p = datos.get('precio')
        if p <= 0:
            raise forms.ValidationError("El precio del servicio no puede ser menor o igual a $0")

        d = datos.get('duracion')
        if d <= 0:
            raise forms.ValidationError("La duracion del servicio debe ser como minimo de 1 modulo")

        descripcion = datos.get('descripcion')
        if re.match(settings.RE_CARACTERES, descripcion) is None:
            raise forms.ValidationError("La descripcion es incorrecta")

        return datos

    class Meta:
        model = ServicioBasico
        fields = (
            "descripcion",
            "precio",
            "duracion",
            "insumos"
        )

        labels = {
            'duracion': '(Duracion en modulos de 15 min)'
        }

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

    def clean(self):
        datos = super(PromoForm, self).clean()

        p = datos.get('precio')
        nombre = datos.get('nombre')
        descripcion = datos.get('descripcion')

        if p <= 0:
            raise forms.ValidationError("El precio de la promoción no puede ser menor o igual a $0")

        if re.match(settings.RE_CARACTERES, nombre) is None:
            raise forms.ValidationError("El nombre es incorrecto")

        if re.match(settings.RE_CARACTERES, descripcion) is None:
            raise forms.ValidationError("La descripcion es incorrecta")

        return datos

    class Meta:
        model = Promocion
        fields = (
            "nombre",
            "descripcion",
            "precio",
            "sector",
            "servicios",
            "imagen",
            "activa"
        )
