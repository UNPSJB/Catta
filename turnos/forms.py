from django import forms
from django.forms import ModelForm
from .models import Turno, TurnoFijo
from personas.models import Empleado
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, MultiField
import datetime
from datetime import timedelta


class CrearTurnoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrearTurnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div('empleado'),
            Div('fecha', css_id='fecha_inicio_simple'),
            Div('cliente'),
            Div('servicios'),
            Div('promociones')
        )
        self.helper.add_input(Submit('crear_turno', 'Crear Turno'))


    def save(self, commit=True):
        datos = super(CrearTurnoForm, self).save()
        return datos

    def clean(self):
        datos = super(CrearTurnoForm, self).clean()

        fecha = datos.get('fecha')
        hora = fecha.time()
        time = datetime.time(00,00,00)
        print(hora)
        print(time)
        if hora == time:
            raise forms.ValidationError("Debe seleccionar una hora para el turno")

        p1 = datos.get('servicios')
        p2 = datos.get('promociones')
        empleado = datos.get('empleado')
        servicios = datos.get('servicios')

        for promocion in p2:
            if (promocion.sector != empleado.sector):
                raise forms.ValidationError("Los servicios deben ser del mismo sector en el que trabaja el empleado")
        for servicio in servicios:
            if (servicio.sector != empleado.sector):
                raise forms.ValidationError("Los servicios deben ser del mismo sector en el que trabaja el empleado")
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


    def clean(self):
        tur = super(ModificarTurnoForm, self).clean()

        turno = self.instance

        servicios = tur.get('servicios')
        cantidad = tur.get('servicios').count()
        print(servicios)
        print(cantidad)
        promociones = tur.get('promociones')
        cantidad1 = tur.get('promociones').count()
        print(promociones)
        print(cantidad1)

        duracion = turno.fecha
        print('inicio del turno')
        print(duracion)

        i = 1

        for i in range(cantidad):
            duracion += servicios[i].get_duracion()

        j=1

        for j in range(cantidad1):
            duracion += promociones[j].get_duracion()

        print('duracion final')
        print(duracion)

        sig_turno = turno.get_proximo_turno(turno)

        if sig_turno!=None:

            print('el turno sig es: ')
            print(sig_turno)

            fecha = sig_turno.fecha

            if duracion > fecha:
                print('entre')
                raise forms.ValidationError("Los nuevos servicios agregados superan el tiempo libre disponible")
        if not servicios and not promociones:
            raise forms.ValidationError("El turno debe tener al menos un servicio o una promocion")

        return tur

    class Meta:
        model = Turno
        fields = {"servicios", "promociones"}


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
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.all(),widget=forms.Select(attrs={'id': 'id_empleado_fijo'}))

    def __init__(self, *args, **kwargs):
        super(CrearTurnoFijoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div('empleado'),
            Div('fecha', css_id='fecha_inicio_fijo'),
            Div('fecha_fin'),
            Div('cliente'),
            Div('servicios'),
            Div('promociones')
        )
        self.helper.add_input(Submit('crear_turno_fijo', 'Crear Turno Fijo'))

    def save(self, commit=True):
        datos = super(CrearTurnoFijoForm, self).save()
        return datos

    def clean(self):

        datos = super(CrearTurnoFijoForm, self).clean()
        p1 = datos.get('servicios')
        p2 = datos.get('promociones')
        empleado = datos.get('empleado')
        servicios = datos.get('servicios')
        for promocion in p2:
            if (promocion.sector != empleado.sector):
                raise forms.ValidationError("Los servicios deben ser del mismo sector en el que trabaja el empleado")
        for servicio in servicios:
            if (servicio.sector != empleado.sector):
                raise forms.ValidationError("Los servicios deben ser del mismo sector en el que trabaja el empleado")
        if not p1 and not p2:
            raise forms.ValidationError("Debe elegir al menos una Promoción o un Servicio")

        fecha = datos.get('fecha')
        hora = fecha.time()
        time = datetime.time(00, 00, 00)
        print(hora)
        print(time)
        if hora == time:
            raise forms.ValidationError("Debe seleccionar una hora para el turno")

        return datos

    class Meta:
        model = TurnoFijo
        fields = {"empleado","fecha", "cliente", "promociones", "servicios", "fecha_fin"}


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
