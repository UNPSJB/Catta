from django import forms
from django.forms import ModelForm
from .models import Turno, TurnoFijo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import datetime
from datetime import timedelta


class CrearTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrearTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_turno', 'Crear Turno'))


    def save(self, commit=True):
        datos = super(CrearTurnoForm, self).save()
        return datos

        #return datos

    def clean(self):
        datos = super(CrearTurnoForm, self).clean()

        p1 = datos.get('servicios')
        p2 = datos.get('promociones')
        if not p1 and not p2:
            raise forms.ValidationError("Debe elegir al menos una Promoción o un Servicio")

        return datos

    class Meta:
        model = Turno
        fields = {"empleado", "cliente", "fecha", "promociones", "servicios"}


class ModificarTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModificarTurnoForm, self).__init__(*args, **kwargs)
        #turno = args.
        #self.auto_id = kwargs.get('auto_id')
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('modificar_turno', 'Modificar Turno'))

    #CORREGIR!!
    '''
    def clean(self):

        fecha = self.instance
        turnos = Turno.objects.all().filter(fecha=fecha)
        turno = turnos.first()
        print(turno)


        turno = super(ModificarTurnoForm, self).clean()
        print(type(turno))
        turno1 = Turno.objects.all().filter(id=self.auto_id)
        print(turno1)
        id = self.auto_id
        print(id)


        empleado = turno.get_empleado()
        sig_turno = turno.get_proximo_turno(self, turno, empleado)

        fecha = turno.fecha
        hora_turno = fecha.time
        duracion = turno.duracion()
        hora_turno += duracion

        fecha1 = sig_turno.fecha
        hora_sig_turno = fecha1.time

        if hora_turno < hora_sig_turno:
            raise forms.ValidationError("Los nuevos servicios agregados superan el tiempo libre disponibñe")
    '''
    class Meta:
        model = Turno
        fields = {"empleado", "servicios", "promociones"}


class EliminarTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EliminarTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        # self.helper.add_input(Submit('eliminar_turno','Eliminar Turno'))

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
        self.helper.add_input(Submit('confirmar_turno', 'Confirmar Turno'))

    class Meta:
        model = Turno
        fields = {"fecha_confirmacion"}


class CrearTurnoFijoForm(ModelForm):

    fecha = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'id': 'fecha_inicio'}))

    def __init__(self, *args, **kwargs):
        super(CrearTurnoFijoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('crear_turno_fijo', 'Crear Turno Fijo'))

    def save(self, commit=True):
        datos = super(CrearTurnoFijoForm, self).save()
        return datos

    def clean(self):
        datos = super(CrearTurnoFijoForm, self).clean()
        p1 = datos.get('servicios')
        p2 = datos.get('promociones')
        if not p1 and not p2:
            raise forms.ValidationError("Debe elegir al menos una Promoción o un Servicio")
        return datos

    class Meta:
        model = TurnoFijo
        fields = {"empleado","fecha", "cliente", "promociones", "servicios","fecha_fin"}


#form_registrar_turno_realizado
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
            'fecha': forms.TextInput(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'servicios': forms.CheckboxSelectMultiple(),
            'promociones': forms.CheckboxSelectMultiple(),
        }

    def save(self, commit=True):
        turno = super(RegistrarTurnoRealizadoForm, self).save()
        turno.save()
        return turno
