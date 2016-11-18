from django import forms
from django.forms import ModelForm
from turnos.models import Turno
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CrearTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrearTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_turno', 'Crear Turno'))

    class Meta:
        model = Turno
        fields = {"fecha", "empleado", "servicios", "promociones", "cliente"}


class ModificarTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModificarTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('modificar_turno','Modificar Turno'))

    class Meta:
        model = Turno
        fields = {"fecha", "empleado", "servicios", "promociones"}

class EliminarTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EliminarTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        #self.helper.add_input(Submit('eliminar_turno','Eliminar Turno'))

    class Meta:
        model = Turno
        fields = {"fecha", "empleado", "servicios", "promociones"}

class DetalleTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DetalleTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('detalle_turno', 'Detalle Turno'))

    class Meta:
        model = Turno
        fields = {"fecha", "empleado", "servicios", "promociones", "cliente"}

class ConfirmarTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConfirmarTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('confirmar_turno','Confirmar Turno'))

    class Meta:
        model = Turno
        fields = {"fecha_confirmacion"}


class RegistrarTurnoRealizadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrarTurnoRealizadoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('registrar_turno', 'Registrar Turno Realizado'))

    class Meta:
        model = Turno
        fields = [
            'servicios',
            'promociones'
        ]
        labels = {
            'fecha': 'Fecha del Turno',
            'cliente': 'Cliente ',
            'servicios': 'Servicios',
            'promociones': 'Promociones',
            'empleado': 'Empleado'
        }
        widgets = {
            'fecha': forms.TextInput(attrs={'class':'form-control'}),
            'empleado': forms.Select(attrs={'class':'form-control'}),
            'cliente': forms.Select(attrs={'class':'form-control'}),
            'servicios': forms.CheckboxSelectMultiple(),
            'promociones': forms.CheckboxSelectMultiple(),
        }

    def save(self, usuario, commit=True):
        turno = super().save(commit=False)
        turno.save()
        return turno
